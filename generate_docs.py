# Dependencies
import subprocess
import re 

# Generate via pdoc
subprocess.run("pdoc --output-dir ./docs src/macroecon_tools".split(" "))
# Manually remove 
to_remove =r"""
<div id="Timeseries.transformations" class="classattr">
                                <div class="attr variable">
            <span class="name">transformations</span>

        
    </div>
    <a class="headerlink" href="#Timeseries.transformations"></a>
    
    

                            </div>
                            <div id="Timeseries.source_freq" class="classattr">
                                <div class="attr variable">
            <span class="name">source_freq</span>

        
    </div>
    <a class="headerlink" href="#Timeseries.source_freq"></a>
    
    

                            </div>
                            <div id="Timeseries.data_source" class="classattr">
                                <div class="attr variable">
            <span class="name">data_source</span>

        
    </div>
    <a class="headerlink" href="#Timeseries.data_source"></a>
    
    

                            </div>
                            <div id="Timeseries.label" class="classattr">
                                <div class="attr variable">
            <span class="name">label</span>

        
    </div>
    <a class="headerlink" href="#Timeseries.label"></a>
    
    

                            </div>
                            <div id="Timeseries.is_percent" class="classattr">
                                <div class="attr variable">
            <span class="name">is_percent</span>

        
    </div>
    <a class="headerlink" href="#Timeseries.is_percent"></a>
    
    

                            </div>
                            <div id="Timeseries.set_percent" class="classattr">
"""
pattern = re.compile(to_remove, re.DOTALL | re.VERBOSE)

with open("docs/macroecon_tools.html", "r") as file:
    content = file.read()

#  Remove the matched content
content = re.sub(pattern, "", content)

# Write the updated content back to the file
with open("docs/macroecon_tools.html", "w") as file:
    file.write(content)