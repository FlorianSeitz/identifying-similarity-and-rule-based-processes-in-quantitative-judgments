# ==========================================================================
# 0 - Preprocesses data from eye tracking studies
# ==========================================================================

rm(list = ls(all = TRUE))

if (!require("pacman")) install.packages("pacman")
pacman::p_load(data.table, stringr, dplyr, bit64)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path)) # changes working directory to folder where this script is

# ==========================================================================
exp <- 1 # needs to be 1 or 2
# ==========================================================================

# ==========================================================================
# Behavioral data
# ==========================================================================

# ==========================================================================
# Get answers

files <- list.files(path = gsub("XX", as.character(exp), "~/Projects/CXCOM-Eye/experiment XX/data/"), full.names = TRUE)
dt <- rbindlist(lapply(files, function(i) {cbind(subj = exp * 100 + as.numeric(strsplit(i, "/| ")[[1]][10]), fread(i, fill = T))}))
colnames(dt) <- c("subj", "Event", "Type",	"Trial_Number",	"Start",	"End",	"Duration",	"Location_X",	"Location_Y",	"Dispersion_X",	"Dispersion_Y",
                    "Plane",	"Avg_Pupil_Size_X",	"Avg_Pupil_Size_Y", "V1", "V2", "V3", "V4")
dt[, End := gsub("[:,]", "", End)]

dt_beh <- dt[grepl("Message", End), paste(End, collapse = ""), by = .(subj, Type)]
dt_beh <- dt_beh[grepl("given response (-?\\d+|unknown)", V1)] # only trials without calibration problem
dt_beh[, block := as.numeric(gsub("\\D", "", str_extract(V1, "block[[:space:]]*\\d+"))) + 1]
dt_beh[, index := 1:.N, by = subj]
dt_beh[, stim := gsub("\\D", "", str_extract(V1, "item[[:space:]]*\\d+"))]
dt_beh[, c("x1", "x2") := lapply(tstrsplit(stim, ""), as.numeric)]
dt_beh[, pos := as.numeric(substring(str_extract(V1, "pos[[:space:]]*-?\\d+"), 4)) + 1]
dt_beh[, c("phase", "var") := tstrsplit(str_extract(V1, "\\w+_\\w+"), "_")]
dt_beh[, phase := ifelse(var == "psych", "psych", ifelse(var == "memory" & index > 200, "test", substr(phase, 1, 5)))]
dt_beh[phase == "psych" & index > 48, phase := "train"]
dt_beh[, var := ifelse(var == "crit", var, "loc")]
dt_beh[, trial := 1:.N, by = .(subj, phase, var)]
dt_beh[, resp := substring(str_extract(V1, "given response (-?\\d+|unknown)"), 16)]
dt_beh[, resp := ifelse(var == "crit", as.numeric(resp), ifelse(resp == "unknown", 0, as.numeric(resp) +1))]
dt_beh[, value := ifelse(var == "loc", pos, ifelse(exp == 1, 5*x1 + x2, round(x1 * x2 * 5/3 + 2))), by = .(subj, index)]
dt_beh[, offset := round(as.numeric(gsub("mid position rt ", "", str_extract(V1, "mid position rt \\d+\\.?\\d*"))), 2)]

dt <- merge(dt, dt_beh[, .(subj, index, Type)])
dt_beh <- dt_beh[!is.na(resp), .(subj, index, phase, var, block, trial, stim, x1, x2, value, resp, corr = value == resp, offset)]

# ==========================================================================
# Get response times

files <- list.files(path = gsub("XX", as.character(exp), "~/Projects/CXCOM-Eye/experiment XX/res/"), full.names = TRUE)
rts <- as.data.table(apply(rbindlist(lapply(files, fread)), 2, function(x) {gsub(" ", "", x)}))
colnames(rts) <- c("subj", "trial", "block", "item", "x1", "x2", "value", "known", "resp", "rt", "offset", "phase", "bonus")
rts[, subj := exp * 100 + as.numeric(subj)]
rts[, block := as.numeric(block) + 1]
rts[, trial := as.numeric(trial) + 1]
rts[, index := 1:.N, by = subj]
dt_beh <- merge(dt_beh, rts[, .(subj, index = as.numeric(index), rt = as.numeric(ifelse(rt == "0", NA, rt)))])

# ==========================================================================
# Get randomizations

rand <- fread(gsub("XX", exp, "~/Projects/CXCOM-Eye/experiment XX/cue_pos_info.csv"))
rand[, c("subj", "x1_index") := .(exp * 100 + V3, V1 + 1)]
rand[, index1_pos := ifelse(subj %% 2 == 0, "right", "left")]
rand[, index1_col := ifelse(subj %% 4 < 2, "purple", "green")]
rand[, x1_pos := ifelse(x1_index == 1, index1_pos, c("left", "right")[c("left", "right") %in% index1_pos == FALSE]), by = subj]
rand[, x1_col := ifelse(x1_index == 1, index1_col, c("green", "purple")[c("green", "purple") %in% index1_col == FALSE]), by = subj]
dt_beh <- merge(dt_beh, rand[, .(subj, x1_pos, x1_col)], by = "subj")

# fwrite(dt_beh, gsub("XX", exp, "../../data/experimentXX-behavioral.csv"))

# ==========================================================================
# Process data
# ==========================================================================

screen_x <- 1920; screen_y <- 1080 # screen in pixels
mid_x <- 415; mid_y <- 235 # center of the exemplar AOIs
size_x <- 320; size_y <- 180; scaling <- 1.2 # size of the AOIs with a scaling factor
size_x <- size_x * scaling; size_y <- size_y * scaling # scales the AOIs
n_bins <- 5 # number of bins

# ==========================================================================
# Looking-at-nothing start and end
# /1 transforms integer64 into integer (pkg: bit64 needs to be loaded)

dt_lan <- merge(dt[grepl("test_crit remove target", End), .(subj, index, lan_start = Start/1)],
                dt[grepl("test_crit response indicated", End), .(subj, index, lan_end = Start/1)])
dt_lan <- merge(dt[Event %in% paste0("Fixation ", c("L", "R"))], dt_lan, by = c("subj", "index"))
dt_lan <- dt_lan[Event == "Fixation R"] # takes only right eye fixations
dt_lan <- dt_lan[(Start <= lan_end) & (End >= lan_start), .(subj, index, frame = Trial_Number, pos_x = Location_X - screen_x/2, pos_y = -(Location_Y - screen_y/2), dur = Duration, fix_start = Start/1, fix_end = as.numeric(End), lan_start, lan_end)]

# ==========================================================================
# Exemplar AOIs: ul = 1, ur = 2, ll = 3, lr = 4; test stimulus = -1; else = 0

dt_lan[, bin := cut(min(lan_end, max(lan_start, (fix_start + fix_end)/2)), # mean truncated fixation time
                    seq(lan_start, lan_end, length.out = n_bins + 1), # split into five bins
                    include.lowest = T, labels = 1:n_bins), by = .(subj, index, frame)]
dt_lan[, lan := ifelse((abs(abs(pos_x) - mid_x) <= size_x/2) & (abs(abs(pos_y) - mid_y) <= size_y/2), # looking at exemplar
                       ifelse(sign(pos_y) == 1, 1, 3) + ifelse(sign(pos_x) == 1, 1, 0), # exemplar position
                       ifelse((abs(pos_x) <= size_x/2) & (abs(pos_y) <= size_y/2), # looking at test stimulus
                              -1, # test stimulus position
                              0))] # any other position (neither exemplar nor test stimulus)
dt_lan[, frame := seq.int(.N), by = .(subj, index)]
dt_lan <- merge(dt_lan, dt_beh[, .(subj, index, stim, resp)], by = c("subj", "index"))

# fwrite(dt_lan, gsub("XX", exp, "../../data/experimentXX-process.csv"))

# ==========================================================================
# Demographics

files <- list.files(path = gsub("XX", as.character(exp), "~/Projects/CXCOM-Eye/experiment XX/info/"), full.names = TRUE)
demos <- rbindlist(lapply(files, function(i) {cbind(subj = exp * 100 + as.numeric(strsplit(i, "_")[[1]][2]), tail(fread(i, fill = T, sep = ";"), 11))}))
colnames(demos)[2] <- "dem" 
demos[grepl("Age", dem), as.numeric(strsplit(strsplit(dem, "/| ")[[1]][2], "'"[[1]][1])), by = subj][subj != "227", sd(V1)]
