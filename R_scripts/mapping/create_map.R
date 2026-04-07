library(leaflet)
library(htmlwidgets)
library(htmltools)
library(jsonlite)

df <- read.csv("../data/2025_geocoded.csv") |> na.omit()
df_json <- toJSON(df, dataframe = "rows")
names_json <- toJSON(sort(unique(df$name)))

js <- readLines("map_render.js") |>
  paste(collapse = "\n") |>
  gsub("MAPDATA_PLACEHOLDER", df_json, x = _, fixed = TRUE) |>
  gsub("NAMELIST_PLACEHOLDER", names_json, x = _, fixed = TRUE)
css <- readLines("map_style.css") |> paste(collapse = "\n")

map <- leaflet(options = leafletOptions(minZoom = 10)) |>
  addTiles() |>
  setView(lng = mean(df$long), lat = mean(df$lat), zoom = 10) |>
  setMaxBounds(
    lng1 = mean(df$long) - 1,
    lat1 = mean(df$lat) - 1,
    lng2 = mean(df$long) + 1,
    lat2 = mean(df$lat) + 1
  ) |>
  onRender(js)

map <- prependContent(
  map,
  tags$link(
    rel = "stylesheet",
    href = "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.css"
  ),
  tags$link(
    rel = "stylesheet",
    href = "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.Default.css"
  ),
  tags$script(
    src = "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/leaflet.markercluster.js"
  ),
  tags$style(css),
  tags$div(
    class = "search-overlay",
    tags$input(
      id = "nameSearch",
      type = "text",
      list = "nameOptions",
      placeholder = "Filter by owner name..."
    ),
    tags$datalist(id = "nameOptions")
  )
)

saveWidget(map, "../exports/2025.html", selfcontained = TRUE)
