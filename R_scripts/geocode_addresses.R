
library(RSQLite)
library(dplyr)
library(tidyr)
library(tidygeocoder)

con <- dbConnect(RSQLite::SQLite(), "../data/tax_data.db")

query <- readr::read_file("../queries/addresses_by_owner_name")
query <- gsub("\\{year\\}", "2025", query)

raw <- dbGetQuery(con, query)
dbDisconnect(con)

processed_df <- raw |>
  separate_longer_delim(property_details, delim = ",") |>
  separate_wider_delim(
    property_details,
    delim = " | ",
    names = c("tax_code", "address")
  ) |>
  mutate(
    address = trimws(address),
    tax_code = trimws(tax_code)
  )

geocoded_results <- processed_df |>
  mutate(
    county = "Champaign",
    state  = "IL"
  ) |>
  geocode(
    street = address,
    county = county,
    state = state,
    method  = "osm",
  )

write_csv(geocoded_results, "./data/owner_properties_geocoded.csv")
