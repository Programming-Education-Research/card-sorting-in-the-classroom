library(tidyverse)
library(DBI)
library(knitr)

question_ordering <- c(
    "Math Expressions",
    "Boolean Reasoning",
    "Dicts",
    "Dicts With Errors",
    "Functional Equivalence",
    "Identify Exceptions",
    "Test Case Match"
)

relabel_courses <- function(course) ordered(
    case_match(course, "CS101" ~ "Compsci 101", "CS130" ~ "Compsci 130"),
    levels = c("Compsci 101", "Compsci 130")
)

relabel_semester <- function(semester) ordered(
    case_match(semester, "SS2025" ~ "Summer Semester", "S12025" ~ "Semester One"),
    levels = c("Summer Semester", "Semester One")
)

relabel_exam <- function(exam) ordered(
    case_match(exam, 1 ~ "Sat Exam", 0 ~ "Did Not Sit"),
    levels = c("Sat Exam", "Did Not Sit")
)

relabel_questions <- function(questions) ordered(
    questions,
    levels = question_ordering
)

t <- function(table) {
    if (isTRUE(getOption('knitr.in.progress'))) {
        return(knitr::kable(table))
    } else {
        return(table)
    }
}


fetch <- function(query) {
    mydb <- dbConnect(RSQLite::SQLite(), "data/database.db")
    raw_data <- dbGetQuery(mydb, query)
    dbDisconnect(mydb)
    return(raw_data)
}


custom_theme <- function(...) (
    theme_minimal()
    + theme(
        plot.title = element_text(face = "bold"),
        axis.text = element_text(colour = "black", face = "bold", size = 10),
        axis.title = element_text(colour = "black", face = "bold", size = 11),
        panel.grid = element_line(
            colour = "black", linetype = "dotted", linewidth = 0.3),
        panel.border = element_rect(linetype = "solid", fill = NA),
        strip.text = element_text(colour = "black", face = "bold", size = 12),
        plot.caption.position = "plot",
        plot.background = element_rect(fill = "white", colour = "white"),
    )
    + theme(...)
)

is_outlier <- function(values) {
    return(values > quantile(values, 0.75) + 1.5 * IQR(values, na.rm = TRUE))
}
