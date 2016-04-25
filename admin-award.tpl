<h2>Award a badge:</h2>
<div id="badgeform">
<form action="" method="POST">
    <p>
    <label for="badge">Badge:</label>
    <select name="badge" required>
        % for badge in badges:
        <option value="{{badge['name']}}">{{badge["name"]}}</option>
        % end
    </select>
    </p>
    <p>
    <label for="user">User:</label>
    <select name="user" required>
        % for user in users:
    	<option value="{{user['email']}}">{{user['email']}}</option>
        % end
	</select>
	</p>
    <input class="submit" type="submit"/>
</div>
</form>



