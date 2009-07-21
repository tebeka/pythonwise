<html>
    <head>
        <title>Tag Cloud</title>
        <style>

            a {
                font-family: Verdana, sans-serif;
                text-decoration: none;
                color: black;
                margin-right: 2px;
            }

            a:hover {
                background-color: silver;
            }
            
            div.cloud {
                width: 80%;
                margin-right: auto;
                margin-left: auto;
                border: 4px solid black;
            }

        </style>
    </head>
    <body>
    <h2><center>Tag Cloud</center></h2>

    <div class="cloud">
        % for tag, fontsize in tags:
            <a href="/tags?tag=${tag}" style="font-size: ${fontsize}">${tag}</a>
        % endfor
    </div>

    </body>
</html>
