<div id="profile">
<div id="parent">  
  <div id="first"><p><div id = "title-text">My Apps</div></p>
    % for app in apps:
	  <table class = "apps">
	  	<colgroup>
	  		<col class = "image">
	  		<col class = "title-col">
	  		<col class = "info-col">
	    </colgroup>
	    <tbody>
	    	<tr>
	    		<td rowspan ="100" style="width: 128px" class = "table-image">
	    			<img src={{apps[app]['image']}} />
	    		</td>
	    	</tr> 
	  		<tr><td class ="title">Name:</td> <td class="info">{{apps[app]['name']}}</td></tr>
	  		<tr><td class ="title">Website:</td> <td class="info"><a href={{apps[app]['website']}}>View</a></td></tr>
	    </tbody>
	  </table>
  % end
</div> 
  <div id="second"><p><div id = "title-text">My Badges</div></p>
  % for badge in badges:
	  <table class = "badge">
	  	<colgroup>
	  		<col class = "image">
	  		<col class = "title-col">
	  		<col class = "info-col">
	    </colgroup>
	    <tbody>
	    	<tr>
	    		<td rowspan ="100" style="width: 128px" class = "table-image">
	    			<img src={{badge['image']}} />
	    		</td>
	    	</tr> 
	  		<tr><td class ="title">Name:</td> <td class="info">{{badge['name']}}</td></tr>
	  		<tr><td class ="title">Issuer:</td> <td class="info">{{badge['issuer']}}</td></tr>
	  		<tr><td class ="title">Description:</td> <td class="info">{{badge['description']}}</td></tr>
	  		<tr><td class ="title">Criteria:</td> <td class="info"><a href={{badge['criteria']}}>View</a></td></tr>
	    </tbody>
	  </table>
  % end
  </div> 
  <div id="third"><p><div id = "title-text">My Progress<div></p>
  </div>
</div>