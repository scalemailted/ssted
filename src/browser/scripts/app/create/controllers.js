async function initControllers(){
    console.log('setup JS contollers')

    const createButton = document.getElementById('create')
    createButton.addEventListener('click', createTnet);

    const degree_distribution = document.getElementById('degree-distribution');
    degree_distribution.addEventListener('change', updateInputs)
    updateInputs()

    const count = await eel.get_count()();
    document.getElementById('counter').innerText = count;

}
 

async function createTnet(){
    console.log('click event')
    const args = getInputs()
    await eel.generate(args)();
    const count = await eel.get_count()();
    document.getElementById('counter').innerText = count;
}

/*
createControllers();
*/


function getInputs(){
    const config = {}

    /*START*/
    //Network Settings
    config.network_density = document.getElementById('network-density').value;
    config.degree_distribution = document.getElementById('degree-distribution').value;
    //Node Settings
    config.nodes_count = document.getElementById('nodes-count').value;
    config.nodes_position = document.getElementById('nodes-position').value;
    config.nodes_velocity = document.getElementById('nodes-velocity').value;
    //Edge Settings
    config.edge_direction = document.getElementById('edge-direction').value;
    config.edge_weights = document.getElementById('edge-weights').value;
    //Event  Settings 
    config.frames_count = document.getElementById('frames-count').value;
    config.events_trigger = document.getElementById('events-trigger').value;
    config.emitter_type = document.getElementById('events-occurence').value;
    config.events_duration = document.getElementById('events-duration').value;
    config.events_min_rate = document.getElementById('events-min-rate').value;
    config.events_activity_rate = document.getElementById('events-activity-rate').value;
    /*END */
    //config.degree_type = document.getElementById('degree-distribution').value;
    //config.node_count = document.getElementById('node-count').value;
    //config.frames = document.getElementById("temporal-duration").value
    switch(config.degree_distribution){
        case "geometric": 
            config.radius = document.getElementById("node-neighbor-radius").value;
            config.mean = document.getElementById("mean").value;
            config.std  = document.getElementById("standard-deviation").value;
            break;
        case "uniform": 
            config.min_degree = document.getElementById("min-degree").value;
            config.max_degree = document.getElementById("max-degree").value;
            break;
        case "gaussian": 
            config.min_degree = document.getElementById("min-degree").value;
            config.max_degree = document.getElementById("max-degree").value;
            break;
        case "powerlaw":
            config.kmin = document.getElementById("k-min").value;
            config.kmax = document.getElementById("k-max").value;
            config.gamma = document.getElementById("gamma").value;
            break;
    }
    return config;
}



function updateInputs(){
    //document.getElementById('input-div').innerHTML = "";
    document.getElementById('edges-options').innerHTML = "";
    new SelectorItem('Edge Directionality','edge-direction','edges-options','unidirectional','directional');
    new InputItem('Edge Weights','edge-weights','1','edges-options');
    
    const degree_distribution = document.getElementById('degree-distribution');
    const selection = degree_distribution.value;
    switch(selection){
        case "geometric": 
            new InputItem("Node Neighbor Radius","node-neighbor-radius","20",'edges-options');
            new InputItem("Mean","mean","0",'edges-options');
            new InputItem("Standard Deviation","standard-deviation","1",'edges-options');
            break;
        case "uniform": 
            new InputItem("Min Degree","min-degree","1",'edges-options');
            new InputItem("Max Degree","max-degree","6",'edges-options');
            break;
        case "gaussian": 
            new InputItem("Min Degree","min-degree","1",'edges-options');
            new InputItem("Max Degree","max-degree","8",'edges-options');
            break;
        case "powerlaw": 
            new InputItem("k min","k-min","1.0",'edges-options');
            new InputItem("k max","k-max","100",'edges-options');
            new InputItem("gamma","gamma","3.0",'edges-options');
            break;
    }

}


initControllers()