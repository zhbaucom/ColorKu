library(shiny)
library(shinydashboard)
library(shinyWidgets)
library(tidyverse)
# setwd("solvRapp")
#GET ALL FUNCTIONS AND DATA FOR APP
source("NYtimesScrape.R")
source("SudokuSolveRplot.R")
source("SudokuSolvR1step.R")
source("SudokuSolvRcomplete.R")
source("sudPlotInit.R")
source("supData.R")
ckList <- readRDS("ckList.RDS")


#APP SPECIFIC SPECIFICATIONS
ColorF <- c("White", "Red", "Orange", "Yellow", "Dark Green", "Light Green", "Dark Blue", "Light Blue", "Dark Purple", "Light Purple")

ColorNum <- c("", 1:9 )
hexCol2 <- c( "#ffffff", "#d62724", "#ff9443", "#eae22d", "#36763e", "#89ca42", "#324590", "#a2ccd5", "#662f9f", "#d2a9be")
ColorDir <- paste("https://color-hex.org/colors/", substr(hexCol2,2, 7), ".png", sep = "")

box_height = "45em"



ui <- dashboardPage(
  dashboardHeader(title = ("Sudoku SolveR")),
  dashboardSidebar(
    selectizeInput("sudType", "Puzzle Type", choices = c("ColorKu", "NY Times", "Custom")),
    uiOutput("PuzOpt"),
    uiOutput("NYtimesOpt"),
    radioGroupButtons("ColNum", "ColorKu or Number Output", choices = c("ColorKu", "Number"), selected = "ColorKu")
  ),
  dashboardBody(
    fluidPage(
      uiOutput("BasePuzzle"),
      box(
        height = box_height,
        uiOutput("uiHead"),
        checkboxGroupInput("plotParams", "Plot Parameters",choices = c("Reveal Colors", "See Only 1"), selected = "See Only 1"),
        plotOutput("Puz"),
        actionGroupButtons(c("Compute", "Reset"), c("Compute", "Reset"), fullwidth = TRUE)
      )
    )
  )
)

server <- function(input, output){

  output$uiHead <- renderUI({
    if(input$sudType == "ColorKu"){
      h3(paste("Difficulty:", ckList$Difficulty[as.numeric(input$ckPuz)]))
    }else if(input$sudType == "NY Times"){
      h3("NY Times Puzzle Published:",paste(format(Sys.Date(), "%a %b %d")))
      }
      
  })
  
  output$NYtimesOpt <- renderUI({
    if(input$sudType == "NY Times")
      radioGroupButtons("emh", "Difficulty", choices = c("easy", "medium", "hard"))
  })
  
  
  v <- reactiveValues(plot = NULL)
  
  cl <- reactiveValues(
    compTime = Sys.time(),
    ResTime = Sys.time()
  )
  
  
  
  observeEvent(input$Compute,{
    v$plot <- pvec() %>%
      SudokuSolveR1step(NoC = input$ColNum) %>%
      sudPlot(reveal = "Reveal Colors" %in% input$plotParams, see1 = "See Only 1" %in% input$plotParams)
    
    cl$compTime <- Sys.time()
  })
  
  observeEvent(input$Reset, {
    if(input$ColNum == "ColorKu"){
      v$plot <- sudPlotInit(pvec())
    }
    
    cl$ResTime <- Sys.time()
  })
  
  pvec <- reactive({
    shiny::validate(
      need(!is.null(input$c81), "Generating...")
    )
    if(input$ColNum == "ColorKu"){
      pvec <- map_chr(paste("c", 1:81, sep = ""), ~input[[.x]])
      ifelse(pvec %in% c("", "White"), NA, PColors[as.numeric(pvec)])
    }
  })
  

  
  output$Puz <- renderPlot({

    if(cl$compTime <= cl$ResTime){
      if(input$ColNum == "ColorKu"){
        
        sudPlotInit(pvec())
      }
    }else{
      v$plot
    }
  })

  
  output$PuzOpt <- renderUI({
    if(input$sudType == "ColorKu"){
      tagList(
        selectizeInput("ckPuz", "ColorKu Puzzles", choices = paste(1:104))
      )
    }
  })
  
  output$BasePuzzle <- renderUI({
    if(input$sudType == "Custom"){
      DefCols <- ""
    }else if(input$sudType == "ColorKu"){
      shiny::validate(
        need(!is.null(input$ckPuz), "Creating input...")
      )
      DefCols <- Number[ckList[[input$ckPuz]]]
      DefCols[is.na(DefCols)] <- ""
    }else if(input$sudType == "NY Times"){
      shiny::validate(
        need(!is.null(input$emh), "Creating input...")
      )
      DefCols <- NYtimes[[input$emh]]
      DefCols[is.na(DefCols)] <- ""
    }
    
    
    PI <- map2(1:81, DefCols, function(cell, sc){
      pickerInput(paste("c", cell, sep = ""), "", multiple = F,
                  choices = ColorNum, selected = sc,
                  
                  choicesOpt = list(content =
                                      mapply(ColorNum, ColorDir, FUN = function(x, y) {
                                        HTML(paste(
                                          tags$img(src=y, width=30, height=30),
                                          x
                                        ))
                                      }, SIMPLIFY = FALSE, USE.NAMES = FALSE)
                                    
                  ))
    })
    
    
    tabBox(
      height = box_height, 
      tabPanel("----Block 1----",
               fluidRow(
                 # h3(paste(DefCols, collapse = ".")),
                 column(3, PI[(0:2)*9 + 1]),
                 column(3, PI[(0:2)*9 + 2]),
                 column(3, PI[(0:2)*9 + 3])
               )),
      tabPanel("----Block 2----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 3]),
                 column(3, PI[(0:2)*9 + 2 + 3]),
                 column(3, PI[(0:2)*9 + 3 + 3])
               )),
      tabPanel("----Block 3----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 6]),
                 column(3, PI[(0:2)*9 + 2 + 6]),
                 column(3, PI[(0:2)*9 + 3 + 6])
               )),
      tabPanel("----Block 4----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 27]),
                 column(3, PI[(0:2)*9 + 2 + 27]),
                 column(3, PI[(0:2)*9 + 3 + 27])
               )),
      tabPanel("----Block 5----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 3 + 27]),
                 column(3, PI[(0:2)*9 + 2 + 3 + 27]),
                 column(3, PI[(0:2)*9 + 3 + 3 + 27])
               )),
      tabPanel("----Block 6----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 6 + 27]),
                 column(3, PI[(0:2)*9 + 2 + 6 + 27]),
                 column(3, PI[(0:2)*9 + 3 + 6 + 27])
               )),
      tabPanel("----Block 7----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 54]),
                 column(3, PI[(0:2)*9 + 2 + 54]),
                 column(3, PI[(0:2)*9 + 3 + 54])
               )),
      tabPanel("----Block 8----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 3 + 54]),
                 column(3, PI[(0:2)*9 + 2 + 3 + 54]),
                 column(3, PI[(0:2)*9 + 3 + 3 + 54])
               )),
      tabPanel("----Block 9----",
               fluidRow(
                 column(3, PI[(0:2)*9 + 1 + 6 + 54]),
                 column(3, PI[(0:2)*9 + 2 + 6 + 54]),
                 column(3, PI[(0:2)*9 + 3 + 6 + 54])
               ))
      
    )
    
    
    
  })
}

shinyApp(ui, server)



