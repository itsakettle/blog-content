library(itsakohonen)
library(data.table)
library(ggplot2)
library(assertthat)
source('lib/neighbours.R')
# Create T data

n <- 10000
t.thickness <- 0.1
dt <- data.table(x=runif(n), y=runif(n))
# dt <- dt[!(x<0.5-(t.thickness/2) & y < (1 - t.thickness)),]
# dt <- dt[!(x>0.5+(t.thickness/2) & y < (1 - t.thickness)),]

ggplot(dt) + 
  geom_point(aes(x=x, y=y), alpha=0.4) +
  ylim(0, 1) + 
  xlim(0, 1)

# (t.thickness*(1-t.thickness) + t.thickness*1)*n
# nrow(dt)

som.grid <- somgrid(10, 1, topo='rectangular')
som.model <- som(as.matrix(dt), grid=som.grid)

plot(som.model, type='changes')
plot(som.model, type='dist.neighbours', draw.arcs=TRUE)

dt.arcs <- SomGridArcs(som.model)

dt.codes <-  as.data.table(som.model$codes)
dt.codes[, code := 1:.N]
dt[, code := som.model$unit.classif]

ggplot(dt, aes(x=x, y=y)) +
  theme(legend.position="none") +
  geom_segment(data=dt.arcs, aes(x=start1, y=start2, xend=end1, yend=end2), alpha=.4) +
  geom_text(aes(label=code, color = as.factor(code)), size=2) +
  geom_label(data=dt.codes, 
             mapping=aes(x=x, y=y, label=code, color = as.factor(code)), 
             size=4)

