SomGridArcs <- function(som) {
  
  assert_that(som$grid$topo == 'rectangular')
  assert_that(som$toroidal == FALSE)
  
  grid <- som$grid$pts
  
  ArcsOfOneCode <- function(i, grid) {

    # Get this code as a vector, call it x
    x <- grid[i, ]
    # create the difference vectors
    mat.grid.less.x <- t(t(grid)-x)
    # Get the distance between x and all the other codes
    distance.from.x <- sqrt(rowSums(mat.grid.less.x*mat.grid.less.x))
    
    # Anything that is less (!) than 2 is a neighbour in a square grid
    neighbours <- which(distance.from.x<2 & distance.from.x!=0)
   
    # We need the codes in order so as to remove
    # duplicates later. Figure out which codes are less than i
    neighbours.less.than.i <- neighbours < i
    
    start.code <- rep(i, length(neighbours))
    end.code <- neighbours
   
    start.code[neighbours.less.than.i] <- neighbours[neighbours.less.than.i]
    end.code[neighbours.less.than.i] <- i
    
    data.table(start.code=start.code, end.code=end.code)
    
  }
  
  dt.arcs <-rbindlist(lapply(1:nrow(grid), ArcsOfOneCode, grid=grid))
  
  # Now remove the duplicates
  dt.arcs <- unique(dt.arcs)
  
  # Now add the locations in the higher dimensional space
  for (i in 1:ncol(som$codes)) {
    start.values <- som$codes[dt.arcs[, start.code], i]
    start.name <- paste0('start', i)
    dt.arcs[, (start.name) := start.values]
    
    end.values <- som$codes[dt.arcs[, end.code], i]
    end.name <- paste0('end', i)
    dt.arcs[, (end.name) := end.values]
  }
  
  dt.arcs
  
}

