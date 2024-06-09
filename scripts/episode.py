# External libraries
import frontmatter

class Episode:
    def __init__(self, file_name):
        with open(file_name) as f:
            self.__episode_frontmatter = frontmatter.load(f)

    def get(self, key):
        return self.__episode_frontmatter.get(key)
