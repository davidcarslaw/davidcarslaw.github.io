# opus revised has London Taxis in
opus <- readRDS("~/My Drive/Projects/Ricardo_rsd/full_data_gpkm.RDS")

opus <- mutate(opus, 
               euro_class = paste("Euro", mvris_euro_status),
               euro_class = case_when(technology == "LNT" ~ "Euro 6 LNT",
                                      technology == "SCR" ~ "Euro 6 SCR",
                                      TRUE ~ euro_class),
               date = parse_date_time(vehicle_manufactured_date, c("dmy", "ymd"))) %>% 
  filter(g_km_nox  > -50, g_km_nox < 100)

# add Euro 6 as a whole
cars_diesel <- opus %>%
  filter(
    mvris_type_approval_category == "M1",
    mvris_fuel_type == "DIESEL",
    NO2_Valid == "V", NO_Valid == "V",
    g_km_nox > -10,
    date > dmy("1/1/1998"),
    !is.na(mvris_euro_status)
  ) 

# Euro status
diesel_euro <- group_by(cars_diesel, euro_class) %>%
  filter(euro_class != "Euro 6") %>% 
  do(bootMeanDF(.$g_km_nox))

ggplot(diesel_euro, aes(euro_class, mean, ymin = min, ymax = max)) +
  geom_bar(stat = "identity", fill = "turquoise4", alpha = 0.6, colour = "turquoise4") +
  geom_pointrange(size = 1.5, col = "deeppink") +
  coord_cartesian(ylim = c(0, 2.2)) +
  xlab("Euro standard") +
  ylab(quickText("nox (g/km)"))

# cars by manufa
diesel_manu <- filter(cars_diesel, euro_class %in% c("Euro 6 LNT", "Euro 6 SCR")) %>%  
  group_by(euro_class, mvris_make) %>%
  do(bootMeanDF(.$g_km_nox)) %>% 
  filter(n > 20) %>% 
  ungroup() %>% 
  mutate(index = row_number())

ggplot(diesel_manu, aes(reorder(index, mean), mean, ymin = min, ymax = max, 
                        fill = euro_class, colour = euro_class)) +
  geom_bar(stat = "identity", alpha = 0.6, width = 0.6) +
  geom_pointrange(col = "grey30") +
  scale_fill_manual(values = c("deeppink", "turquoise4")) +
  scale_color_manual(values = c("deeppink", "turquoise4")) +
  coord_cartesian(ylim = c(0, 3)) +
  xlab("Manufacturer") +
  ylab(quickText("nox (g/km)"))+
  theme(axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        panel.grid.minor = element_blank(), panel.grid.major.x = element_blank())

# cars by manufa
diesel_euro5 <- filter(cars_diesel, euro_class %in% c("Euro 5")) %>%  
  group_by(mvris_make) %>%
  do(bootMeanDF(.$g_km_nox)) %>% 
  filter(n > 20) %>% 
  ungroup() %>% 
  mutate(index = row_number())

ggplot(diesel_euro5, aes(reorder(index, mean), mean, ymin = min, ymax = max)) +
  geom_bar(stat = "identity", alpha = 0.6, width = 0.6, 
           fill = "turquoise4", colour = "turquoise4") +
  geom_pointrange(col = "grey30") +
  coord_cartesian(ylim = c(0, 3)) +
  xlab("Manufacturer") +
  ylab(quickText("nox (g/km)")) +
  theme(axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        panel.grid.minor = element_blank(), panel.grid.major.x = element_blank())


diesel_para <- filter(cars_diesel, 
                      euro_class %in% c("Euro 5", "Euro 6", "Euro 6 LNT", "Euro 6 SCR")) 

id <- which(diesel_para$euro_class %in% c("Euro 6 LNT", "Euro 6 SCR"))
diesel_para$euro_class[id] <- "Euro 6"

diesel_para <- group_by(diesel_para, euro_class, mvris_make) %>%
   summarise(nox = mean(g_km_nox, na.rm = TRUE), n = n()) %>% 
   ungroup()

diesel_para <- gather(diesel_para, key = key, value = value, 3:4) %>% 
  unite(euro_key, c(euro_class, key))

diesel_para <- spread(diesel_para, key = euro_key, value = value) %>% 
  na.omit() 

names(diesel_para)[c(3, 5)] <- c("Euro_5", "Euro_6")
diesel_para$n <- diesel_para[[2]] + diesel_para[[4]]
diesel_para <- select(diesel_para, mvris_make, Euro_5, Euro_6, n)

ggplot(arrange(diesel_para, desc(n)), aes(x = Euro_5, y = Euro_6, size = n, fill = n)) +
  geom_point(shape = 21, alpha = 0.9, colour = "white") +
  xlim(0, 2.25) +
  ylim(0, 1.75) +
  scale_fill_viridis_c(option = "plasma") +
  geom_abline(intercept = 0, slope = 1, lty = 5) +
  scale_size_area(max_size = 25) +
  theme(legend.position = "none") +
  xlab(quickText("Euro 5 nox (g/km)")) +
  ylab(quickText("Euro 6 nox (g/km)"))
