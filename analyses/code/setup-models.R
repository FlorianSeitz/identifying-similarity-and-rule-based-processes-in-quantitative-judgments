# ==========================================================================
# Setup: Cognitive models
# Author: Florian I. Seitz
# ==========================================================================

## Set up the models -------------------------------------------------------
#  Standard RULEX-J model (Bröder et al. 2017)
RULEX_J <- function(dt, ll_bool, sim = TRUE, rule = TRUE) {
  
  # defines admissible parameter range
  pars <- c(if(rule) {c(b0 =  0)}, b1 =  5, b2 =  5, if(rule & sim) {c(alpha = .5)}, sigma =  1)
  lb <-   c(if(rule) {c(b0 =-10)}, b1 =  0, b2 =  0, if(rule & sim) {c(alpha = 0)},  sigma =  0)
  ub <-   c(if(rule) {c(b0 = 10)}, b1 = 10, b2 = 10, if(rule & sim) {c(alpha = 1)},  sigma = 10)

  # defines equality constraints on alpha for pure rule and similarity models
  eq_fun <- NULL; eq_B <- NULL
  # if(sim) {
  #   eq_fun <- function(pars, d, ll_bool, sim, rule, predict) {
  #     return(c(pars[["alpha"]], pars[["b0"]]))
  #   }
  #   eq_B <- c(1, 0)
  # }
  # if(rule) {
  #   eq_fun <- function(pars, d, ll_bool, sim, rule, predict) {
  #     return(pars[["alpha"]])
  #   }
  #   eq_B <- 0
  # }
  
  # fits the model
  m <- solnp(pars = pars, fun = fit_fun, LB = lb, UB = ub, eqfun = eq_fun, eqB = eq_B,
             d = dt, ll_bool = ll_bool, sim = sim, rule = rule)
  
  # makes model predictions with optimal parameter estimates
  out <- fit_fun(m$pars, dt, predict = TRUE, sim = sim, rule = rule)
  
  return(list(list(var = c(names(m$pars), "ll_train", "ll_test"),
                   val = c(m$pars, -1 * tail(m$values, 1), -1 * fit_fun(m$pars, dt, ll_bool = (1-ll_bool), sim = sim, rule = rule))),
              list(stim = out$stim,
                   preds = out$pred,
                   obs = out$resp,
                   is_fit = ll_bool)))
}

#  Pure similarity model
SIM <- function(dt, ll_bool) {
  RULEX_J(dt = dt, ll_bool = ll_bool, sim = TRUE, rule = FALSE)
}

#  Pure similarity model
RULE <- function(dt, ll_bool) {
  RULEX_J(dt = dt, ll_bool = ll_bool, sim = FALSE, rule = TRUE)
}