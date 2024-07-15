# ==========================================================================
# 1 - Behavioral analyses
# ==========================================================================

if (!require("pacman")) install.packages("pacman")
pacman::p_load(data.table, stringr, dplyr, ggplot2, latex2exp, splithalf, ggtext, patchwork)
theme_set(theme_classic())

# change working directory to folder where this script is
setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) 

# defines functions for summary statistics
m_sd <- function(x, dig = 2) {return(list(m = round(mean(x), dig), mdn = round(median(x), dig), sd = round(sd(x), dig)))}
rng <- function(x, dig = 2) {return(list(min = round(min(x), dig), max = round(max(x), dig)))}

# ==========================================================================
exp <- 2 # specify experiment; needs to be 1 or 2
# ==========================================================================

dt_beh <- fread(gsub("X", exp, "../../data/processed/experimentX-behavioral.csv"))[resp != -1]
dt_lan <- fread(gsub("X", exp, "../../data/processed/experimentX-process.csv"))[resp != -1]
modeling <- readRDS(gsub("X", exp, "../../analyses/other/experimentX-models.rds"))

# defines variable if test stimulus is old exemplar or new stimulus
ex <- dt_beh[phase == "train" & var == "crit", unique(stim)] # gets exemplars
dt_beh[phase == "test" & var == "crit", type := ifelse(stim %in% ex, "old", "new")] 

# ==========================================================================
# Exemplar Representation

# computes the number of training blocks needed and the accuracy achieved
ex_res <- dt_beh[phase != "psych" & paste0(var, type) != "critnew", .( 
  n = max(block), acc = mean(corr)), by = .(subj, phase = paste(phase, var, sep = "_"))]
ex_res[, m_sd(n, 0), by = phase] # number of blocks per phase
ex_res[, m_sd(100*acc, 0), by = phase] # accuracy per phase

# correlates location and criterion accuracy and combines them into one variable "exemplar accuracy"
ex_res_wide <- dcast(ex_res[grepl("test", phase)], subj ~ phase, value.var = "acc")
ex_res_wide[, cor.test(test_crit, test_loc, method = "kendall")] # correlation location and criterion accuracy
ex_res_wide[, test_acc := (test_crit + test_loc) / 2] # computes exemplar accuracy
ex_res_wide[, c(m_sd(test_acc), shapiro.test(test_acc)[1:2])] # descriptive statistics of exemplar accuracy (see Table 1)

# ==========================================================================
# Looking-At-Nothing, grouped by subj and old vs. new test stim

# summary statistics
dt_beh[phase == "test", mean(offset, na.rm = T), by = subj][, m_sd(V1, 0)] # test stimulus presentation time
dt_lan[, any(lan > 0), by = .(subj, index)][, mean(V1), by = subj][, m_sd(V1)] # % trials with looking-at-nothing
dt_lan[, unique((lan_end - lan_start)/1000), by = .(subj, index)][, mean(V1), by = subj][, m_sd(V1, 0)] # time from test stimulus removal to reaching the response scale

# computes looking-at-nothing duration
standardize_by_all <- F # TRUE or FALSE (FALSE is reported in main text) 
lan <- if(standardize_by_all) { # Standardizes looking-At-nothing at whole duration
  dt_lan[, .(lan, stim = ifelse(stim %in% ex, "old", "new"), prop = dur/sum(dur)), by = .(subj, index, id = stim)]
} else { # Standardizes looking-At-nothing at duration to exemplars + test stimulus
  dt_lan[lan != 0, .(lan, stim = ifelse(stim %in% ex, "old", "new"), prop = dur/sum(dur)), by = .(subj, index, id = stim)]
}
lan <- lan[, .(prop = sum(prop)), by = .(subj, index, id, stim, lan = ifelse(lan == -1, "center", ifelse(lan == 0, "none", "ex")))]
lan <- dcast(lan, subj + index + id + stim ~ lan, fill = 0)
lan[, .(m = mean(ex)), by = subj][, c(m_sd(m), shapiro.test(m)[1:2])] # descriptive statistics of looking-at-nothing (see Table 1)

# compares looking-at-nothing for old and new test stimuli
lan_by_stim <- dcast(lan[, .(m = mean(ex)), by = .(subj, stim)], subj ~ stim)
lan_by_stim[, cor.test(old, new, method = "kendall")] # correlation looking-at-nothing for old and new test stimuli

# correlates looking-at-nothing with exemplar accuracy
lan_acc <- merge(lan[, .(lan = mean(ex)), by = subj], ex_res_wide)
lan_acc[, cor.test(lan, test_acc, method = "kendall")]

# computes split-half reliability for looking-at-nothing for even and odd trials
lan <- merge(lan, dt_beh[phase == "test" & var == "crit", .(subj, index, block)], by = c("subj", "index"))
lan[, block_bool := ifelse(block %% 2 == 0, "even", "odd")]
reliability <- splithalf(data = lan, outcome = "accuracy", score = "average", halftype = "oddeven", 
                         conditionlist = unique(lan$id), var.ACC = "ex", var.participant = "subj", var.condition = "id",
                         var.compare = "block_bool", compare1 = "odd", compare2 = "even")
as.data.table(reliability$Estimates)[, m_sd(splithalf)]

# ==========================================================================
# Association looking-at-nothing and cognitive modeling

fits <- modeling[, res[[1]][[1]], by = .(subj, model, oos)] # gets parameter estimates and log likelihoods
preds <- modeling[, res[[1]][[2]], by = .(subj, model, oos)] # gets trial-level predictions

fits[var == "ll_test", median(val), by = .(subj, model)][, m_sd(V1), by = .(model)]
preds[is_fit == 0, preds - obs, by = .(subj, model, stim)][, .(
  MAE = mean(abs(V1)), RMSE = sqrt(mean(V1^2))), # computes the mean absolute error and root mean square error of the model predictions
  by = .(subj, model)][, as.list(round(colMeans(.SD), 2)), by = .(model), .SDcols = !"subj"]

# computes summary statistics for the alpha estimates
alphas <- fits[model == "rulex_j" & var == "alpha", .(alpha = mean(val)), by = subj] # gets mean alpha estimate across cross-validations by participant
alphas[, c(m_sd(alpha), shapiro.test(alpha)[1:2])] # descriptive statistics of alpha (see Table 1)
alphas[, t.test(alpha, mu = .50)] # tests alpha against .50 (valid in main experiment because sample size > 30)
alphas[, class := cut(alpha, breaks = c(0, .1, .5, .9, 1), include.lowest = T)] # clusters alpha into groups

# !! correlates looking-at-nothing with looking-at-nothing !!
lan_alpha <- merge(lan_acc, alphas)
lan_alpha[, cor.test(lan, alpha, method = "kendall")] # main correlation
lan_alpha[alpha %between% c(.1, .9), c(N = .N, cor.test(lan, alpha, method = "kendall")[4:3])] # correlation for .1 < alpha < .9

# creates Figure 3
labels <- data.table(alpha = c(.025, .3, .7, .975), 
                     lan = .85, 
                     label = c("rs", "rw", "sw", "ss"))
labels[, label := factor(label, levels = c("rs", "rw", "sw", "ss"), labels = c("Rule\n(strong)", "Rule\n(weak)", "Similarity\n(weak)", "Similarity\n(strong)"))]
ggplot(lan_alpha, aes(x = alpha, y = 100*lan)) + 
  geom_point(alpha = ifelse(lan_alpha[, alpha %between% c(.1, .9)], 1, 1)) +
  geom_vline(xintercept = c(.1, .5, .9), lty = 2, color = "grey") +
  geom_label(data = labels, aes(label = label, color = label), size = 3) +
  stat_smooth(data = lan_alpha, method = "lm", se = FALSE, color = grey(0, .5)) +
  scale_color_manual(values = viridis::cividis(6, begin = .15, end = .9, direction = -1)[c(1, 2, 5, 6)]) +
  scale_x_continuous(name = "Cognitive modelling", breaks = c(0, .1, .5, .9, 1), limits = c(-.05, 1.05), expand = c(0, 0),
                     labels = c("\u03b1 = 0\nRule", "\u03b1 = .1", "\u03b1 = .5\nMixture", "\u03b1 = .9", "\u03b1 = 1\nSimilarity")) +
  scale_y_continuous(name = "Looking-at-nothing (in %)", limits = c(-2.5, 100), expand = c(0, 0)) +
  labs(x = "Cognitive modelling", y = "% LAN", color = "Classification") + theme(legend.position = "none")
# ggsave(gsub("X", exp, "../../analyses/figures/figure3.png"), width = 6, height = 2.5)

# ==========================================================================
# Discussing the participants who attended to only one cue

ws <- fits[model == "rulex_j" & var %in% c("b1", "b2"), .( # looks at the estimated attention weights of RulEx-J
  var, val = val / sum(val)), # normalizes the estimated attention weights
  by = .(subj, oos)][var == "b1", .(
    w1 = median(val)), by = .(subj)] # computes the median normalized attention weight for each participant
unidim <- ws[round(abs(w1 - .5), 2) == .5, subj] # defines participant ids who attended to only one cue
dt_beh[subj %in% unidim & phase == "test" & var == "crit", # looks at the criterion test phase of these 4 participants
       mean(resp == DescTools::Mode(resp)), by = .(subj, ifelse(subj %in% unidim[1:3], x2, x1))][, mean(V1)]
pars_unidim <- fits[subj %in% unidim & model == "rulex_j", mean(val), by = .(subj, var)] # gets the mean parameter estimates for each of these four participants
pars_unidim[var == "alpha", m_sd(V1)] # computes the mean alpha estimate for the four participants
lan_alpha[subj %in% unidim, m_sd(lan)] # computes the mean looking-at-nothing of these four participants
lan_alpha[!subj %in% unidim, cor.test(lan, alpha, method = "kendall")] # computes correlation looking-at-nothing and alpha without these four participants

# ==========================================================================
# Model comparison

# computes AIC weights for each model and participant
models <- c("rule", "sim", "rulex_j") # defines the models
gofs <- fits[var == "ll_test", .(ll = median(val)), by = .(subj, model)] # gets the median out-of-sample log likelihood by participant
gofs <- gofs[, .(model, exp(ll - max(ll))), by = .(subj)][, .(model, weight = V2 / sum(V2)), by = .(subj)] # transforms the median ll into an AIC weight

gofs <- merge(gofs, lan_alpha[, .(subj, alpha, lan)])
setorderv(gofs, cols = c("alpha"), order = 1)
gofs[, m_sd(weight), by = model] # summary aic weights (Table C2)

# compares looking-at-nothing for people with alpha < or > .5
lan_alpha[, .(.N, mean(lan)), by = .(alpha > .5)]
lan_alpha[, wilcox.test(lan ~ (alpha > .5))]
lan_alpha[!subj %in% unidim, wilcox.test(lan ~ (alpha > .5))]

# computes looking-at-nothing and responses to critical stimuli for rule and similarity users (Table 2)
critical <- c(11, 12, 34, 44) # defines the critical test stimuli
dt_beh_alpha <- merge(dt_beh[phase == "test" & var == "crit" & stim %in% critical], lan_alpha)
dt_beh_alpha[, mean(resp), by = .(subj, group = alpha > .5, stim)][, m_sd(V1), by = .(group, stim)]
dt_beh_alpha[, mean(resp - value), by = .(subj, group = alpha > .5, stim)][, m_sd(V1), by = .(group, stim)]

# makes Figure C1
gofs[, ord := as.numeric(factor(subj, levels = unique(subj), labels = 1:length(unique(subj))))]
gofs[, model := factor(model, levels = models, labels = c("Rule model", "Similarity model", "RulEx-J model"))]

ggplot(gofs, aes(x = ord, y = weight)) +
  geom_bar(aes(fill = model), stat = "identity", color = "black", size = 0.25) +
  scale_fill_manual(values = viridis::cividis(3, begin = .2, end = .8, direction = -1)[c(1, 3, 2)], name = "Model") +
  xlab(" ") +
  ylab("Evidence") +
  theme(
    axis.ticks.x = element_blank(),
    axis.text.x = element_blank(),
    axis.line = element_blank(), 
    panel.grid = element_blank(),
    panel.border = element_blank(),
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 11),
    legend.title = element_text(size = 14),
    legend.text = element_text(size = 12)) +
  scale_x_continuous(limits = c(0.5, 48.5), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0, 1.001), breaks = c(0, .25, .5, .75, 1), expand = c(0, 0))
# ggsave("../../analyses/figures/fig-evidence.png", width = 6.6, height = 4)

# ==========================================================================
# Properties

# ==========================================================================
# a. Temporal dynamics
dt_lan[, lan2 := ifelse(lan <= 0, lan, 1)]
dt_lan <- merge(dt_lan, alphas, by = "subj")
dt_lan[, best := factor(alpha > .5, labels = c("Rule", "Similarity"))]

# computes looking-at-nothing duration for each time bin and model
lan_bin <- melt(dcast(dt_lan[, sum(dur), by = .(subj, best, index, stim, bin, lan2)], subj + best + index + stim + bin ~ lan2, fill = 0), id.vars = c("subj", "best", "index", "stim", "bin"), variable.name = "lan")
lan_bin <- lan_bin[lan != 0, .(lan, prop = value/max(sum(value), .Machine$double.eps)), by = .(subj, best, index, stim, bin)]
lan_bin <- lan_bin[lan == 1, .(prop = mean(prop)), by = .(subj, best, bin)]

# compares looking-at-nothing duration for various time bins
lan_bin[, shapiro.test(prop), by = .(best, bin)] # normality test
lan_bin[, m_sd(prop), by = .(best, bin)] # looking-at-nothing duration for each time bin and model
lan_bin[, wilcox.test(prop ~ best)[c("statistic", "p.value")], by = bin]
lan_bin[, wilcox.test(prop[bin == 5], prop[bin == 4])]

# makes facet a of Figure 4
(plot1 <- ggplot(lan_bin, aes(bin, 100 * prop, color = best, fill = best)) +
    stat_summary(fun = mean, geom = "line", aes(group = best), size=.8, lty = 1) +
    stat_summary(fun = mean, geom = "point", aes(group = best), size=3, shape = 21) +
    stat_summary(fun.data = mean_se, geom = "errorbar", width = .2, size = 1) +
    scale_x_discrete(limits = factor(1:5)) +
    scale_color_manual(values = viridis::cividis(2, begin = .2, end = .8, direction = -1)) +
    scale_fill_manual(values = viridis::cividis(2, begin = .2, end = .8, direction = -1)) +
    ggtitle("(a) Within-trial temporal dynamics") +
    labs(x = "Time bin within trial", y = "Looking-at-nothing (in %)", color="", fill = "") +
    theme(panel.grid = element_blank(), legend.position = "none"))

# ==========================================================================
# b. Relation to similarity
lan_sim <- melt(dcast(dt_lan[, sum(dur), by = .(subj, best, index, stim, lan)], subj + best + index + stim ~ lan, fill = 0), id.vars = c("subj", "best", "index", "stim"), variable.name = "lan")
lan_sim <- lan_sim[lan != 0, .(lan, prop = value/max(sum(value), .Machine$double.eps)), by = .(subj, best, index, stim)]

# computes looking-at-nothing and similarity to every exemplar using each participants parameter estimates
lan_sim <- merge(lan_sim, unique(dt_beh[phase == "train" & var == "loc" & stim %in% ex, .(subj, ex = stim, x1, x2, lan = as.factor(value))]), by = c("subj", "lan"))
ws <- fits[model == "rulex_j" & var %in% c("b1", "b2"), median(val), by = .(subj, var)][, .(w1 = V1[1]/sum(V1)), by = .(subj)]
lan_sim <- merge(lan_sim, ws, by = "subj")
lan_sim[, dist := w1 * abs(floor(stim/10) - x1) + (1-w1) * abs((stim %% 10) - x2)]

# computes correlation between distance to exemplar and looking-at-nothing to exemplar location
lan_sim[best == "Similarity", cor.test(dist, prop, method = "kendall")]
lan_sim[best == "Rule", cor.test(dist, prop, method = "kendall")]
lan_sim_agg <- lan_sim[, .(prop = mean(prop)), by = .(subj, best, large = dist > 1, ex == stim)]
lan_sim_agg[, m_sd(prop), by = .(best, ex, large)]
lan_sim_agg[, wilcox.test(prop ~ best)[c("statistic", "p.value")], by = .(ex, large)]

# computes looking-at-nothing strength
lan_strength <- lan_sim[, prop[dist == min(dist)]/max(sum(prop), .Machine$double.eps), by = .(subj, best, index)][, .(strength = mean(V1)), by = .(subj, best)]
lan_strength[, m_sd(strength), by = .(best)]
lan_strength[, c(m_sd(strength), shapiro.test(strength)[1:2])] # descriptive statistics for looking-at-nothing strength (Table 1)
lan_strength[, wilcox.test(strength ~ best)] # compares looking-at-nothing strength between similarity and rule users

lan_alpha <- merge(lan_alpha, lan_strength)
lan_alpha[, cor.test(alpha, strength, method = "kendall")] # correlates looking-at-nothing strength

# makes facet b of Figure 4
(plot2 <- ggplot(lan_sim, aes(x = dist, y = 100 * prop, color=best, fill = best)) +
    geom_smooth(data = lan_sim[, .(prop = mean(prop)), by = .(dist, best, subj)], method = "gam", level = .95) +
    ggtitle("(b) Relation to similarity") +
    labs(color = "", fill = "") +
    scale_color_manual(values = viridis::cividis(2, begin = .2, end = .8, direction = -1)) +
    scale_fill_manual(values = viridis::cividis(2, begin = .2, end = .8, direction = -1)) +
    scale_x_continuous(name = "Exemplar's distance from test stimulus", limits = c(0, 3), breaks = c(0:3), expand = c(0, 0)) +
    scale_y_continuous(name = "Looking-at-nothing (in %)", expand = c(0, 0)) +
    theme(strip.text.x = element_text(size = 5),
          strip.background = element_rect(size=.5)) +
    theme(strip.text.x = element_text(margin = margin(.01, 0, .01, 0, "cm")),
          panel.grid = element_blank(), legend.position = "none")
)

# ==========================================================================
# c. Distribution across exemplars

# computes the number of trials in which 0-4 exemplars were looked at
lan_nstim <- merge(dt_lan[, .(best = unique(best)), by = .(subj, index)], dt_lan[lan >= 1, .(n_ex = length(unique(lan))), by = .(subj, index)], all = T)
lan_nstim[is.na(n_ex), n_ex := 0]
lan_nstim <- lan_nstim[, .N, by = .(best, n_ex)]
lan_nstim[, .(sum(N[n_ex != 0]), sum(N)), by = best][, prop.test(V1, V2)] # proportion of trials with looking-at-nothing for similarity and rule users
lan_nstim[n_ex != 0, .(sum(N[n_ex == 1]), sum(N)), by = best][, prop.test(V1, V2)] # proportion of trials with looking-at-nothing at one exemplar for similarity and rule users
lan_sim[, .(sum(prop > 0), prop[dist == min(dist)] > 0), # computes how many exemplars were looked at and if the most similar exemplar was looked at
        by = .(subj, best, index)][V1 == 1, .( # if only one exemplar was looked at,
          sum(V2), .N), by = best][, prop.test(V1, N)] # compares the proportion of trials were most similar exemplar was looked at for rule and similarity users
lan_sim[, .(sum(prop > 0), max(prop) == prop[dist == min(dist)], max(prop) / sum(prop)), by = .(subj, best, index)][V1 > 1][, .(sum(V2), .N), by = best][, prop.test(V1, N)] 

lan_nstim <- lan_nstim[, .(n_ex, perc = N/sum(N)), by = best]

# makes facet c in Figure 4
(plot3 <- ggplot(lan_nstim, aes(n_ex, 100 * perc, color = best, fill = best)) +
    geom_bar(stat = "identity", position = position_dodge(.8), size = 1, width = .65) +
    geom_text(aes(label = round(100 * perc)), vjust = -0.3, position = position_dodge(.8), size = 4) +
    ggtitle("(c) Distribution across exemplars") +
    labs(x = "Number of exemplar locations looked at", color = "", fill = "") +
    scale_color_manual(values = viridis::cividis(2, begin = .2, end = .8, direction = -1), guide = "none") +
    scale_fill_manual(values = viridis::cividis(2, begin = .2, end = .8, direction = -1, alpha = .4), guide = "none") +
    scale_y_continuous(name = "% of trials", expand = c(0, 0), limits = c(0, 100)) +
    theme(axis.ticks.x = element_blank()))

plot1 + plot2 + plot3 + plot_layout(guides = "collect") & 
  theme(axis.title = element_text(size = 13), axis.text = element_text(size = 12), title = element_text(size = 14))
ggsave("../../analyses/figures/figure4.png", width = 12.5, height = 4.5)
