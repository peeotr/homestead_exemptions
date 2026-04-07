library(dplyr)

df <- read.csv("./data/2025_geocoded.csv")

duplicates <- df |>
  group_by(address, name) |>
  summarise(count = n(), .groups = "drop") |>
  filter(count > 1) |>
  arrange(desc(count))

write.csv(duplicates, "./data/duplicate_addresses.csv", row.names = FALSE)
