# Loading Libraries
library(arules)
library(arulesViz)
library(RColorBrewer)

# import dataset
data("Groceries")

# using apriori() function
rules <- apriori(Groceries,
                 parameter = list(supp = 0.01, conf = 0.2))

# using inspect() function
inspect(rules[1:5])

# using itemFrequencyPlot() function
arules::itemFrequencyPlot(Groceries, topN = 7,
                          col = brewer.pal(8, 'Pastel2'),
                          main = 'Relative Item Frequency Plot',
                          type = "relative",
                          ylab = "Item Frequency (Relative)")
