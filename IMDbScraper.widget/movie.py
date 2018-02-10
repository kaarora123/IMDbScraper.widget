class Movie(object):
    """
    A movie object stores a movie's title, genres, and description.
    """
    def __init__(self, title, genres, description):
        """
        Initializes a Movie object.
        title: string, movie's title
        genres: list of strings, movie's genres
        description: string, movie's description
        """
        self.title = title
        self.genres = genres
        self.description = description
        
    
    def __eq__(self, other):
        """
        Checks if one Movie object is equal to another based on the movie's title.
        
        return: boolean
        
        """
        if isinstance(self, other.__class__):
            return self.title == other.get_title()
        return False
    
    def __hash__(self):
        """
        Creates a hash value for the Movie object based on the movie's title.
        return: int, hash value
        
        """
        return hash(self.title)
    
    def get_title(self):
        
        """
        return: string, the movie's title  
        
        """
        return self.title

    def get_genre(self):
        """
        return: a list of strings, movie's genres
        
        """
        return self.genres

    def get_description(self):
        """
        return: string, the movie's description
        
        """
        return self.description
    
    def __str__(self):
        """
        Creates a new div element for the movie. 
        
        return: string, a div element that will be used to display the movie
        """
        div = ("<div class='movie'>"+
        "<div class='title'>" + self.title + "</div>" +
        "<div class='genres'>" + ' '.join(map(str, self.genres)) + "</div>" +
        "<div class='description'>" + self.description + "</div>" + 
        "</div> <hr/>")
        
        return div
