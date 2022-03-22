
sudPlotInit <- function(puz){
  puz  %>%
    matrix(9,9,byrow = TRUE)%>%
    data.frame() %>%
    rownames_to_column("i") %>%
    gather("j", "Value", X1:X9) %>%
    mutate(
      i = -as.integer(i), 
      j = as.numeric(substr(j, 2, 2)),
      Value = ifelse(is.na(Value), "White", Value)
    )%>%
    ggplot(aes(x = j, y = i, color = Value))+ 
    coord_fixed() + 
    xlim(c(.5,9.5)) + 
    ylim(c(-9.5,-.5)) + 
    geom_hline(yintercept = -3.5, size = 2) +
    geom_hline(yintercept = -6.5, size = 2) +
    geom_vline(xintercept = 3.5, size = 2) +
    geom_vline(xintercept = 6.5, size = 2) +
    geom_point(color = "black", size = 16) +
    geom_point(size = 15) +
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

