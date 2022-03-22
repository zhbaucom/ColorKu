library(shiny)
library(shinydashboard)
library(shinyWidgets)
library(tidyverse)

ColorF <- c("White", "Red", "Orange", "Yellow", "Light Green", "Dark Green", "Light Blue", "Dark Blue", "Light Purple", "Dark Purple", "White")

ColorNum <- c("", 1:9 )
hexCol <- c( "#ffffff", "#d62724", "#ff9443", "#eae22d", "#89ca42", "#36763e", "#a2ccd5", "#324590", "#d2a9be", "#662f9f")
ColorDir <- paste("https://color-hex.org/colors/",substr(hexCol,2, 7), ".png", sep = "")





ui <- dashboardPage(
  dashboardHeader(),
  dashboardSidebar(
    selectizeInput("sudType", "Puzzle Type", choices = c("Custom", "ColorKu")),
    uiOutput("PuzOpt"),
    radioGroupButtons("ColNum", "ColorKu or Number Output", choices = c("ColorKu", "Number"), selected = "ColorKu"),
    checkboxGroupInput("plotParams", "Plot Parameters",choices = c("Reveal Colors", "See Only 1")),
    actionButton("run", "Run")
  ),
  dashboardBody(
    fluidRow(
      uiOutput("BasePuzzle"),
      box(
        plotOutput("InitBoard")
      ),
      fluidRow(
        box(width = 10,
          plotOutput("CompPuz")
        )
        
      )
   )
)
)

server <- function(input, output){

  pvec <- reactive({
    if(input$ColNum == "ColorKu"){
      pvec <- map_chr(paste("c", 1:81, sep = ""), ~input[[.x]])
      ifelse(pvec == "", NA, PColors[as.numeric(pvec)])
    }
  })
  
  comPuzdone <- eventReactive(input$run,{
    pvec() %>%
      SudokuSolveR1step(NoC = input$ColNum) %>%
      sudPlot(reveal = "Reveal Colors" %in% input$plotParams, see1 = "See Only 1" %in% input$plotParams)
  })
  
  output$CompPuz <- renderPlot({
    comPuzdone()
  })
  
  output$InitBoard <- renderPlot({
    if(input$ColNum == "ColorKu"){
      sudPlotInit(pvec())
    }
  })
  
  output$PuzOpt <- renderUI({
    if(input$sudType == "ColorKu"){
      tagList(
        selectizeInput("ckPuz", "ColorKu Puzzles", choices = c("1", "82"))
      )
    }
  })
  
  output$BasePuzzle <- renderUI({
  if(input$sudType == "Custom"){
    DefCols <- ""
  }else if(input$sudType == "ColorKu"){
    DefCols <- Number[ckList[[input$ckPuz]]]
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



