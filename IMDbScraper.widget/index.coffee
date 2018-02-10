
command: "/usr/local/bin/python IMDbScraper.widget/scraper.py"

refreshFrequency: 43200000 #refresh every 12 hours

render: (_) -> """

	<h1>Which movies would you like to see?</h1>
	<div class="movies">
	</div>

"""

update: (output, domEl) ->

	data = JSON.parse output

	#get the movies in local storage
	for movie, i in localStorage
		$(".movies").append(localStorage.getItem(localStorage.key(i)))


	for movie, i in data
		beginTitleTag = movie.indexOf("title") + 7
		endTitleTag = movie.indexOf("<", beginTitleTag)
		movieTitle = movie.substring(beginTitleTag, endTitleTag)

		#if the movie is in local storage, don't do anything
		if localStorage[movieTitle] != undefined
			console.log("movie in storage")
		else
			$(".movies").append(movie)
	

	$(domEl).find(".movie").on "click", -> 

  	if $(this).hasClass("highlighted")
  		 $(this).removeClass("highlighted")
  		 localStorage.removeItem($(this).find(".title").text())
  	else 
  		$(this).addClass("highlighted")
  		localStorage.setItem($(this).find(".title").text(), $(this)[0].outerHTML + "<hr/>")





style: """
	bottom: 125px
	left: 25px

	h1
		width: 300px
		color: #E2E8ED
		text-align: center
		background-color: rgba(0, 0, 0, 0.5)
		font-family: Futura
		font-size: 20px
		border-radius: 10px

	.movie
		color: white
		font-family: Courier
		padding: 2px
		padding-left: 4px
	

	.title
		font-size: 14px

	.genres
		font-size: 9px

	.description
		font-size: 10px;

	.movies
		height: 200px
		width: 300px
		overflow: scroll
		background-color: rgba(0, 0, 0, 0.4)
		border-radius: 10px

	hr
		margin:0

	.highlighted
		background-color: rgba(30, 213, 58, 0.4)



"""
