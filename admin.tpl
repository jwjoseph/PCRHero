<h2>Create a badge:</h2>
<div id="badgeform">
<form action="" method="POST">
    <p>
    <label for="name">Name of the Badge:</label>
    <input type="text" name="name" size="30" required/> </p>
    <p>
    <label for="description">Description:</label>
    <textarea name="description" rows="2" cols="30" required style="vertical-align: top;"> </textarea> </p>
    <p>
    <label for="image">Image:</label>
    <input type="file" name="image" accept="image/png" size="30" required/>
  	</p>
    <p>
    <label for="criteria">Criteria:</label>
    <textarea name="criteria" rows="2" cols="30" required style="vertical-align: top;"> </textarea></p>
    <p>
    <label for="tags">Tags:</label>
    <input type="text" name="tags" size="30" required/> </p>
    <p>
    <label for="issuer">Issuer:</label>
    <select name="issuer" required> 
    	<option value="pcrhero">PCR Hero</option>
	</select>
	</p>
    <input class="submit" type="submit"/>
</div>
</form>



