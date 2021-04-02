function initControllers(){
    console.log('setup JS contollers')

    const selector = document.getElementById('location-selector')

    updateSelector()

    const submit_btn = document.getElementById('analyze-button')
    submit_btn.addEventListener('click',analyzeTnet)

    eel.clear_data()();
}


async function updateSelector(){
    const selector = document.getElementById('location-selector')
    selector.innerHTML = ""
    selector.innerHTML += `<option default value='local'>Local</option>`
    count = await eel.get_count()()
    console.log("tnet_count",count)
    for (let i=1; i<=count; i++){
        const label = await eel.get_description(i)();
        selector.innerHTML += `<option value='${i}'>${i}:${label}</option>`
    }
}


async function analyzeTnet(){
    console.log('click event')
    const tnet = document.getElementById('location-selector').value
    await eel.analyze(tnet)();
    visuals = document.getElementById('analysis-visuals');
    visuals.innerHTML = `<img class='img-fluid' src='../data/temporal_degree_centrality.png'>
                         <img class='img-fluid' src='../data/temporal_degree_centrality_overall.png'>
                         <img class='img-fluid' src='../data/topological_overlap_overall.png'>
                         <img class='img-fluid' src='../data/topological_overlap.png'>
                         <img class='img-fluid' src='../data/topological_overlap_average.png'>
                         <img class='img-fluid' src='../data/temporal_correlation_coefficient.png'>
                         <img class='img-fluid' src='../data/icts_avg_lag.png'>
                         <img class='img-fluid' src='../data/icts_max_lag.png'>
                         <img class='img-fluid' src='../data/bursty_coeff.png'>
                         <img class='img-fluid' src='../data/bursty_coeff_avg.png'>
                         <img class='img-fluid' src='../data/lvs.png'>
                         <img class='img-fluid' src='../data/lvs_avg.png'>
                         <img class='img-fluid' src='../data/shortest_paths.png'>
                         <img class='img-fluid' src='../data/tcc.png'>
                         <img class='img-fluid' src='../data/tbc.png'>`
}


initControllers()



/*Classes */
class FolderLoader{
    constructor(containerID ='source-input', ext='.json'){
        document.getElementById(containerID).innerHTML = "" +
        `<input id="folder-uploader" type="file" name='file' webkitdirectory directory multiple>`
        this.folderUpload = document.getElementById('folder-uploader');
        this.folderUpload.addEventListener('change', () => this.getFiles(ext) )
    }
    async getFiles( ...extensions){
        const data = [];
        let files = [ ...this.folderUpload.files].filter( f=> extensions.some( ext => f.name.includes(ext)) )
        for (let file of files){
            const jsonString = await file.text();
            const json = JSON.parse(jsonString)
            data.push(json);
        }
    this.load(data)
    }
    load(data){
        //separate out this function
        let networks = data.map( item => new Graph(item.nodes, item.links))
    }
}

class SourceSelector{
    constructor(id='location-selector'){
        this.networks = [];
        this.selector = document.getElementById(id);
        this.selector.addEventListener('change', () => this.update() )
        this.update();
    }
    async update(){
        switch(this.selector.value){
            case 'local': new FolderLoader(); break;
            default: 
                const tnet = await eel.get_tnet(this.selector.value)()
                new AppLoader(tnet); break;
                //new AppLoader(this.selector.value); break;
        }
    }
}
