
sudPlot <- function(compPuz, reveal = FALSE, see1 = TRUE){
  sbs <- compPuz %>%
    map2(names(.),function(x, y){
      if(y %in% c("OriginalPuzzle", "CompletedPuzzle")){
        out <- x %>%
          data.frame() %>%
          rownames_to_column("i") %>%
          gather("j", "Value", X1:X9) %>%
          mutate(
            i = -as.integer(i), 
            j = as.numeric(substr(j, 2, 2)),
            Value = ifelse(is.na(Value), "White", Value)
          )
        out[[paste(y, "Value", sep = "")]] <- ifelse(is.na(out$Value), "White", out$Value)
        out %>%
          select(-Value)
      }
      
    })
  
  Value <- ifelse(reveal, "CompletedPuzzleValue","OriginalPuzzleValue")
  
  inner_join(sbs$OriginalPuzzle, sbs$CompletedPuzzle, by = c("i", "j")) %>%
    mutate(Update = OriginalPuzzleValue != CompletedPuzzleValue) %>%
    group_by(Update) %>%
    mutate(
      see1n = see1,
      Update2 = Update & sample(c(TRUE, rep(FALSE, length(Update)-1))),
      Update = ifelse(see1n, Update2, Update)
    ) %>%
    ungroup() %>%
    mutate(
      i.new = ifelse(Update, i, NA),
      j.new = ifelse(Update, j, NA),
      CompletedPuzzleValue = ifelse((OriginalPuzzleValue != "White") | Update, CompletedPuzzleValue, "White")
    ) %>%
    ggplot(aes_string(x = "j", y = "i", color = Value))+ 
    coord_fixed() + 
    geom_hline(yintercept = -3.5, size = 2) +
    geom_hline(yintercept = -6.5, size = 2) +
    geom_vline(xintercept = 3.5, size = 2) +
    geom_vline(xintercept = 6.5, size = 2) +
    geom_point(color = "black", size = 16) +
    geom_point(size = 15) +
    geom_point(aes(x = j.new, y = i.new), color = "black", shape = 4, size = 2, stroke = 2) +
    scale_color_manual(breaks = PColors, values = hexCol) +
    theme_bw() +
    theme(
      legend.position = "none", 
      panel.grid.major = element_blank(), 
      panel.grid.minor = element_blank(),
      axis.title.x=element_blank(),
      axis.text.x=element_blank(),
      axis.ticks.x=element_blank(),
      axis.title.y=element_blank(),
      axis.text.y=element_blank(),
      axis.ticks.y=element_blank(),
      panel.background = element_rect(fill = "#BAAC95")
    ) + 
    coord_fixed() + 
    xlim(c(.75,9.25)) + 
    ylim(c(-9.25,-0.75))
}

