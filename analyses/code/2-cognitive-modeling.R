# ==========================================================================
# 2 - Cognitive modeling
# ==========================================================================

# ==========================================================================
exp <- 2 # specify experiment: 1 (= additive) or 2 (= multiplicative)
parallel <- TRUE # fit on a parallel machine (Unix) or single core
# ==========================================================================

if (!require("pacman")) install.packages("pacman")
pacman::p_load(data.table, modelr, purrr, devtools, cognitiveutils, doRNG, Rsolnp, stringr, truncnorm)
if (parallel == TRUE) pacman::p_load(doFuture)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) # changes working directory to folder where this script is

d <- fread(gsub("X", exp, "../../data/processed/experimentX-behavioral.csv"))[resp != -1]
ex <- unique(d[phase == "train" & var == "crit", .(stim, x1, x2, value)])

d <- d[phase == "test" & var == "crit"]

# ==========================================================================
# Makes objective function and equality constraints for attention weights
# ==========================================================================
fit_fun <- function(pars, d, ll_bool = NULL, sim = TRUE, rule = TRUE, predict = FALSE) {
  b1 <- pars["b1"]; b2 <- pars["b2"]; sigma <- pars["sigma"]

  if (sim) { # computes similarity process
    sims <- d[, .(ex[, x1] - unique(x1), ex[, x2] - unique(x2), value = ex[, value]), by = stim]
    sims[, s := exp(-(b1 * abs(V1) + b2 * abs(V2)))] # computes the similarity
    sims[, s := s / sum(s), by = stim] # normalizes the similarity
    sim_process <- sims[, .(sim_pred = sum(value * s)), by = stim]
  }
  
  if (rule) { # computes rule process
    b0 <- pars["b0"]
    rule_process <- d[, .(rule_pred = b0 + b1 * unique(x1) + b2 * unique(x2)), by = stim]
  }
  
  if (sim & rule) { # combines processes
    alpha <- pars["alpha"]
    out <- merge(sim_process, rule_process)[, .(stim, pred = alpha * sim_pred + (1-alpha) * rule_pred)]
  } else {
    if (sim)  {out <- sim_process[, .(stim, pred = sim_pred)]}
    if (rule) {out <- rule_process[, .(stim, pred = rule_pred)]}
  }
  out <- merge(d, out)[order(index)]
  
  if (predict) return(out)
  ll <- dnorm(x = out$resp, mean = out$pred, sd = sigma, log = TRUE)
  ll[is.na(ll)] <- 0
  return(sum(c(-ll_bool * ll)))
}
# pars <- c(b0 = 0, b1 = 1, b2 = 1, alpha = .5, sigma = 1)

# ==========================================================================
# Specifies to-be-fitted models
# ==========================================================================
source("setup-models.R")
model_list <- list(
  rulex_j = RULEX_J,  # RULEX-J (Bröder et al. 2017)
  sim = SIM,          # RULEX-J with alpha = 1 (pure similarity model)
  rule = RULE         # RULEX-J with alpha = 0 (pure rule model)
)

# ==========================================================================
# Makes cross-validation data sets cv_data for each participant
# ==========================================================================
oos <- sort(unique(d[, stim]))

# ==========================================================================
# Fits models
# ==========================================================================
if (parallel == TRUE) {
  registerDoFuture()
  plan(multisession, workers = 4L)  ## on MS Windows
  fits <- foreach(x = unique(d$subj),
                  .combine = "rbind",
                  .inorder = FALSE, 
                  .packages = c("data.table", "modelr", "devtools", "Rsolnp", "truncnorm"),
                  .export = c("model_list", "ex", "oos", "RULEX_J", "fit_fun")) %dorng% {
                    source("setup-models.R", local = TRUE)
                    curr_d <- d[(subj == x), ]
                    
                    do.call("rbind", lapply(oos, function (curr_oos) {
                      ll_bool <- curr_d[, as.numeric(stim %in% curr_oos == FALSE)]
                      curr_d[, .(
                        oos = curr_oos,
                        model = names(model_list),
                        res = map(model_list, exec, dt = .SD, ll_bool = ll_bool)), by = subj]
                    }))
                  }
} 

# saveRDS(fits, gsub("X", exp, "../../analyses/other/experimentX-models.rds"))

# ==========================================================================
# Access model fitting results the following way:
# ==========================================================================
fits[, res[[1]][[1]], by = .(subj, oos, model)] # parameters + goodness-of-fit (ll)
fits[, res[[1]][[2]], by = .(subj, oos, model)] # predictions
