rm(list=ls())
library(data.table)
library(ggplot2)

dt <- fread('data/Make Model Data 2016.csv', skip=4)
View(dt[, sum(Total), by=.(VehicleMake, VehicleModel, YearOfBirth)])

# Get the top 5 vehicle makes
top_five_vehicle_makes <- dt[, .(total=sum(Total)), 
                             by=.(VehicleMake)][order(-total),][1:5, VehicleMake]

dt_pass_rate_by_year <- dt[, .(total=sum(Total),
                               pass=sum(PASS),
                               pass_rate=sum(PASS)/sum(Total)), by=YearOfBirth]

ggplot(dt_pass_rate_by_year, aes(x=YearOfBirth, y=pass_rate)) + 
  geom_line() +
  geom_text(aes(size=total, label=YearOfBirth))

dt_pass_rate_by_year <- dt[VehicleMake %in% top_five_vehicle_makes
                           & YearOfBirth > 1995, 
                           .(total=sum(Total),
                             pass=sum(PASS),
                             pass_rate=sum(PASS)/sum(Total)), by=.(YearOfBirth)]

ggplot(dt_pass_rate_by_year, aes(x=YearOfBirth, y=pass_rate)) + 
  geom_line() +
  geom_point(aes(size=total))

dt_pass_rate_by_year_by_make <- dt[VehicleMake %in% top_five_vehicle_makes
                                   & YearOfBirth > 1995
                                   & YearOfBirth < 2012, 
                                 .(total=sum(Total),
                                   pass=sum(PASS),
                                   pass_rate=sum(PASS)/sum(Total)), by=.(YearOfBirth, VehicleMake)]

ggplot(dt_pass_rate_by_year_by_make, aes(x=YearOfBirth, y=pass_rate, color=VehicleMake)) + 
  geom_line() +
  geom_point(aes(size=total))

setkeyv(dt_pass_rate_by_year_by_make, c('VehicleMake', 'YearOfBirth'))
dt_pass_rate_by_year_by_make[, delta := c(NA, diff(pass_rate)), by=.(VehicleMake)]

ggplot(dt_pass_rate_by_year_by_make, aes(x=YearOfBirth, y=delta, color=VehicleMake)) + 
  geom_line() +
  geom_point(aes(size=total))
