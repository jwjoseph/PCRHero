<h2>Upload an image:</h2>
<div class="images-wrapper">
	<div id="badgeform">
	<form method="POST" enctype="multipart/form-data">
		<p>
	    <label for="image">Image:</label>
	    <input type="file" name="image" accept="image/png" size="30" required/>
	  	</p>
	    <input class="submit" type="submit"/>
	</div>
	<div id="image-display">
		%for image in images:
		<div id = "image-group">
		<div id="image-name">{{image}}</div><img src={{'http://www.pcrhero.org:8000/images/' + image}} />
		</div>
		%end
	</div>
</div>
</form>


