<h2>Assign a task:</h2>
% if(typeselection == 0):
<div id="badgeform">
<form action="" method="POST">
    <p>
        <label for="typeselection">Task type:</label>
    <select id="typeselection" name="typeselection" required>
        <option value="percent">Percent increase</option>
        <option value="repeat">Repeat task</option>
        <option value="unique">Unique tasks</option>
        <option value="time trial">Time trial</option>
        <option value="performance">Performance/Efficiency</option>
    </select>
    </p>
    <input name="flag" type="hidden" value="False"> 
    <input class="submit" type="submit"/>
</div>
% else:
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
    <p>
    <label for="app">App:</label>
    <select name="app" required>
        % for app in app_list:
        <option value="{{app}}">{{app}}</option>
        % end
    </select>
    </p>
    %if(typeselection == "percent"):
    <p>
        <label for="circuit">Circuit:</label>
        <input name="circuit" type="text" required>
        </p>
        <p>
        <label for="score">Initial score:</label>
        <input name="score" type="text" required>
        </p>
        <p>
        <label for="percent">Percent Improvement:</label>
        <input type="range" id = "percent-slider" min="0" max="500" value="0" step="5" onchange="showValue('percent-slider', 'percent')"/>
        <input name="percent" id = "percent" type="text" style="width:30px;" value="100" required>
    </p>
    %elif(typeselection == "repeat"):
    <p>
        <label for="repeat">Repetitions:</label>
        <input name="repeat" type="text"  required>
        </p>
        <p>
        <label for="circuit">Circuit:</label>
        <input name="circuit" type="text" required>
    </p>
    %elif(typeselection == "unique"):
    <p>
        <label for="unique">Unique circuits:</label>
        <input name="unique" type="text"  required>
    </p>
    %elif(typeselection == "performance"):
    <p>
        <label for="targetyield">Desired Pathway Yield:</label>
        <input name="targetyield" type="text"  required>
        </p>
        <p>
        <label for="cost">Cost:</label>
        <input name="cost" type="text"  required>
        </p>
        <p>
        <label for="circuit">Circuit:</label>
        <input name="circuit" type="text" required>
    </p>
    %else:
        <p>
            <label for="day-slider">Days: </label>
            <input type="range" id="day-slider" min="0" max="7" value="0" step="1" onchange="showValue('day-slider', 'days')"/>
            <input type="text" id="days" name="days" value="0" style="width:20px;" required>
        </p>
        <p>
            <label for="hour-slider">Hours: </label>
            <input type="range" id="hour-slider" name="hours" min="0" max="23" value="0" step="1" onchange="showValue('hour-slider', 'hours')" />
            <input type="text" id="hours" name="hours" value="0" style="width:20px;" required>
        </p>
        <p>
            <label for="minute-slider">Minutes: </label>
            <input type="range" id="minute-slider" name="minutes" min="0" max="59" value="0" step="1" onchange="showValue('minute-slider', 'minutes')" />
            <input type="text" id="minutes" name="minutes" value="0" style="width:20px;" required>
        </p>        
        <p>
        <label for="tasknum">Number of tasks:</label>
        <input name="tasknum" type="text"  required>
        </p>
        <p>
        <label for="circuit">Circuit:</label>
        <input name="circuit" type="text" required>
        </p>
    %end
        <script>
            function showValue(sliderID, textbox)
            {
                var x = document.getElementById(textbox);
                var y = document.getElementById(sliderID);
                x.value = y.value;
            }
        </script>
    <input name="flag" type="hidden" value="True"> 
    % finaltype = typeselection
    <input name="typeselection" type="hidden" value={{finaltype}}>
    <input class="submit" type="submit"/>
</div>
% end
</form>

