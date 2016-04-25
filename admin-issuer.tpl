<div class="issuer-menu">
    <div id="badgeform">
        <h2>Create an issuer:</h2>
        <form action="" method="POST">
            <p>
            <label for="name">Name of the Organization:</label>
            <input type="text" name="name" size="30" pattern="([a-zA-Z]|_)+" title="Letters only - underscore for space" required/> </p>
            <p>
            <label for="description">Description:</label>
            <textarea name="description" rows="2" cols="30" required style="vertical-align: top;"> </textarea></p>
            <p>
            <label for="url">URL:</label>
            <input type="url" name="url" size="30" required/> </p>
            <input class="submit" type="submit"/>
        </form>
    </div>
    <div id ="issuer-list">
        <h2>Current issuers:</h2>
        <ul>
        % for issuer in issuers:
        <li>{{issuer}}</li>
        %end
        </ul>
    </div>
</div>



