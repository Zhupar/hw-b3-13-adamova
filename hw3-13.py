class HTML:
    def __init__(self,tag):
        self.tag = "html" 
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self 
                
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        f = open("index.html", "w")
        f.write(str(self))
        f.close()

    def __str__(self):
        html = "<{}>\n".format(self.tag)
        for child in self.children:
            html += str(child)
        html += "\n</{}>".format(self.tag)
        return html


class TopLevelTag (HTML):
    def __init__(self,tag, *args, **kwargs):
        self.tag = tag 
        self.children = []
    

class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
    
        
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __iadd__(self, other):
        self.children.append(other)
        return self


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
    
    def __str__ (self, *args, **kwargs):
        attr=""
        for attribute, value in self.attributes.items():
            attr+=f"{attribute} = \"{value}\" "

        if len(self.children) > 0:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attr)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}>".format(tag=self.tag, attrs=attr)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attr, text=self.text
                )

if __name__ == "__main__":
    with HTML("html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body