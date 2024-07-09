# ==========================================================================
# Parameter recovery for alpha in the multiplicative environment
# ==========================================================================

if (!require("pacman")) install.packages("pacman")
pacman::p_load(data.table, ggplot2, patchwork, Rsolnp, pracma)
set.seed(321)

# recreates the environment
env <- function(x1, x2) {
  round(5/3 * x1 * x2 + 2) # true multiplicative function that links cues and criterion
}
dt <- as.data.table(expand.grid(x1 = 1:4, x2 = 1:4)) # possible cue values
dt[, id := 1:.N] # id for each stimulus

ex <- data.table(x1 = c(1, 2, 3, 4), x2 = c(4, 1, 2, 3)) # exemplar cue values
ex[, crit := env(x1, x2)] # exemplar criterion values
ex <- unique(merge(ex, dt))

# computes the similarity process
computes_sim <- function(pars, dt, y = ex) {
  b1 <- pars["b1"]; b2 <- pars["b2"]
  sims <- dt[, .(sim = exp(-(b1 * abs(x1 - y[, x1]) + b2 * abs(x2 - y[, x2])))), by = id]
  sims[, sum(sim * y[, crit]) / sum(sim), by = id][, V1]
}

# computes the rule process
computes_rule <- function(pars, dt) {
  dt[, pars["b0"] + pars["b1"] * x1 + pars["b2"] * x2]
}

# combines the two processes
predicts <- function(pars, sim, rule) {
  alpha <- pars["alpha"]
  pred <- alpha * sim + (1-alpha) * rule
  rep(pred, each = 8) # repeats predictions 8 times as in experiment
}

# builds model
model <- function(pars, dt, ex, resps) {
  sim <- computes_sim(pars, dt, ex)
  rule <- computes_rule(pars, dt)
  preds <- predicts(pars, sim, rule)
  return(-sum(dnorm(resps, preds, sd = pars[["sigma"]], log = T)))
}

# defines simulation variables
nreps <- 500 # number of simulation iterations
alphas <- seq(0, 1, .1) # true alpha values

res <- as.data.table(do.call("rbind", lapply(1:nreps, function(rep) {
  print(paste0("-------------- Iter: ", rep, "/", nreps, " --------------"))
  
  # samples a parameter value combination and computes the similarity and rule process predictions
  pars_i <- c(alpha = NA, b0 = runif(1, -10, 10), b1 = runif(1, 0, 10), b2 = runif(1, 0, 10), sigma = runif(1, 0, 10))
  print(round(pars_i, 2))
  sim <- computes_sim(pars_i, dt)
  rule <- computes_rule(pars_i, dt)
  
  # combines the similarity and rule processes according to alpha
  do.call("rbind", lapply(alphas, function(alpha) { # samples through true alpha values
    pars_i[["alpha"]] <- alpha
    preds <- predicts(pars_i, sim, rule) # makes prediction with current alpha
    resps <- round(preds + rnorm(length(preds), sd = pars_i[["sigma"]])) # adds noise to responses

    m <- solnp(pars = c(alpha = .5, b0 = 0, b1 = 5, b2 = 5, sd = 1),
               LB = c(0, -10, 0, 0, 0), UB = c(1, 10, 10, 10, 10), 
               fun = model, dt = dt, ex = ex, resps = resps)
    
    data.table(iter = rep,
               par = names(pars_i),
               true = pars_i,
               fit = m$pars,
               gof = tail(m$values, 1)
    )
  }))
})))

fwrite(res, "../../analyses/other/parameter-recovery.csv")

res[, rmserr(true, fit), by = par][, round(.SD, 2), by = par]
res[par == "alpha", cor(true, fit), by = iter][, summary(V1)]

res[par == "alpha" & true == .5, mean(fit)]
res[par == "alpha" & true != .5, .5 %between% sort(c(true, fit)), by = paste0(iter, "-", true)][, 1 - mean(V1)]

res[par == "alpha", lm(fit~true)$coefficients[["true"]], by = iter][, summary(V1)]
res[, true0 := true - .5]
res[par == "alpha", lm(fit~true0)$coefficients[["(Intercept)"]], by = iter][, summary(V1)]

theme_set(theme_classic())
ggplot(res[par == "alpha" & iter <= 100], aes(true, fit)) +
  geom_abline(intercept = 0, slope = 1, lty = 2) +
  # geom_boxplot() +
  geom_point(alpha = .05) +
  geom_line(aes(group = iter), alpha = .05) +
  stat_summary(fun.data = mean_se, geom = "errorbar", width = .05) +
  stat_summary(fun.data = mean_se, geom = "point", size = 3) +
  stat_summary(fun.data = mean_se, geom = "line", size = 1) +
  scale_x_continuous(name = expression(True~alpha~value), limits = c(0, 1),
                     labels =  c("Rule\n\u03b1 = 0", "\n\u03b1 = .25", "Mix\n\u03b1 = .5", "\n\u03b1 = .75", "Similarity\n\u03b1 = 1")) +
  scale_y_continuous(name = expression(Estimated~alpha~value), limits = c(0, 1)) +
  coord_equal()
ggsave("../lan-ex/figures/alpha-recovery.png", width = 5, height = 5)

ggplot(res[par == "alpha"], aes(as.factor(true), fit)) +
  geom_boxplot(outlier.color = grey(.4, .2)) +
  scale_x_discrete(name = expression(True~alpha~value)) +
  scale_y_continuous(name = expression(Estimated~alpha~value), limits = c(0, 1), breaks = seq(0, 1, .1))
ggsave("Projects/lan-ex/figures/alpha-recovery2.png", width = 5, height = 5)

ggplot(res[par == "alpha"], aes(true, fit)) +
  geom_abline(intercept = 0, slope = 1, lty = 2) +
  stat_summary(fun.data = mean_se, geom = "errorbar", width = .05) +
  stat_summary(fun.data = mean_se, geom = "point", size = 3) +
  # stat_summary(fun.data = mean_se, geom = "line", size = 1) +
  scale_x_continuous(name = expression(True~alpha~value), limits = c(0, 1),
                     labels =  c("Rule\n\u03b1 = 0", "\n\u03b1 = .25", "Mix\n\u03b1 = .5", "\n\u03b1 = .75", "Similarity\n\u03b1 = 1")) +
  scale_y_continuous(name = expression(Estimated~alpha~value), limits = c(0, 1)) +
  coord_equal()
ggsave("../lan-ex/figures/alpha-recovery.png", width = 5, height = 5)
