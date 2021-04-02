//Canvas to render onto
class D3Canvas{
    constructor(width=window.innerWidth, height=600, id='#chart'){
        this.margin = {top: -20, right: 5, bottom: 5, left: 5};
        this.width = width - this.margin.right - this.margin.left;
        this.height = height - this.margin.top - this.margin.bottom;
        this.load(id);
    }

    load(id='#chart'){
        this.modal = d3.select(id);
        this.addSVG();
        this.addPath();
        this.addCircle();
    }

    addSVG(){
        this.svg = this.modal.append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)
            .append("g")
            .attr("class", "everything") 
            //.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
    }
    addPath(){
        this.pathG = this.svg.append("g")
            .attr("class", "pathG")
    }
    addCircle(){
        this.circleG = this.svg.append("g")
            .attr("class", "circleG")
    }
}



class Graph{
    constructor(nodes, links){
        this.nodes = nodes;
        this.links = links;
        const fill = `${this.links.length}`.length
        this.links.forEach( e => e.id= +(1+ e.source.padStart(fill,0)+e.target.padStart(fill,0) ))
        this.linkedById = {};
        this.links.forEach( d => this.linkedById[`${d.source},${d.target}`] = 1 );
        this.simulation = d3.forceSimulation(this.nodes) 
            .force("link", d3.forceLink(this.links).id( d=>d.id ))
    }
    isConnected(a, b) {
        //console.log(this.linkedById)
        return this.linkedById[`${a.id},${b.id}`] || this.linkedById[`${b.id},${a.id}`] || a.id === b.id;
    }
}

class NetworkViewer extends D3Canvas{
    constructor(width=window.innerWidth, height=600, id='#chart'){
        super(width,height,id);
        this.radius = this.width * 0.4;
        this.nodeRadius = 3;
        //add zoom capabilities 
        this.zoom_actions = this.zoom_actions.bind(this);
        //this.tickActions = this.tickActions.bind(this);
        this.fade = this.fade.bind(this);
        //const self = this;
        const zoom_handler = d3.zoom().on("zoom", () => this.zoom_actions() );
        zoom_handler(this.modal)
        //this.timeSlider = new TemproalSlider();
        //this.timeSlider.register(this);
        this.duration = 250;
        this.activeNode = null;
    }

    update(graph) {
        //console.log(graph)
        this.graph = graph;
        this.linkedById = graph.linkedById;
        this.nodes = graph.nodes;
        this.links = graph.links;
        this.simulation = graph.simulation;
        
            //.force('charge', d3.forceManyBody(-100))
            //.force("center", d3.forceCenter(width / 2, height / 2))
        //this.simulation.on("tick", this.tickActions );
        this.simulation.tick(1);
        //graph.load(this.width, this.height)
        //const {nodes, links} = graph;
        this.updateCircles(this.nodes);
        this.updatePaths(this.links);
      }

    updateCircles(nodes){
        let circle = this.circleG.selectAll('circle').data(nodes, d=>d.id);
        circle.exit().remove();

        const entered_circle = circle
            .enter().append('circle')
            .attr('r', this.nodeRadius)
            .attr('stroke-width', 0.5)
            .attr('stroke', 'white')
            .attr('fill', 'red')
            .attr('cx', d=>d.x)
            .attr('cy', d=>d.y)
            .on('mouseover.fade', d => this.fade(0.1,d) )
            .on('mouseout.fade', d => this.fade(1,d) )
          
        circle = circle.merge(entered_circle);

        circle.transition().ease(d3.easeCircle).duration( this.duration ) //1000
            .attr('cx', d=>d.x)
            .attr('cy', d=>d.y)
            .attr('id', d=>`node-${d.id}-`);
      }

    updatePaths(links){
        let path = this.pathG.selectAll('path').data(links, d=>d.id);
        path.exit().remove();

        //console.log(path)
        const entered_path = path
            .enter().append('path')
            .attr('stroke-linecap', 'round')
            .attr('stroke-width', '0.75px')
            .attr('stroke', 'green')
            .attr('opacity', 1)
            .attr('fill', 'transparent')
            .attr('class', 'link')
            .on('mouseout.fade', d => this.fade(1,d))

        //console.log('path',path, 'entered path',entered_path)
        path = path.merge(entered_path);

        this.pathG.selectAll('path')
            .style('opacity', o =>  (this.activeNode?.id == o.target.id || this.activeNode?.id == o.source.id || this.activeNode == null) ? 1 : 0.1 )

        //path.attr('opacity', o =>  (this.activeNode == o.target || this.activeNode == o.source || this.activeNode == null) ? 1 : 0.1 )

        path.transition().ease(d3.easeCircle).duration( this.duration ) //1000
          .attr('id', d=>  `link-source-${d.source.id}-target-${d.target.id}-`)
          .attr('stroke', 'mediumblue')
          .attr("d", d => `M${d.source.x},${d.source.y}L${d.target.x},${d.target.y}`)


            
    }
    //Zoom functions 
    zoom_actions(){
        this.svg.attr("transform", d3.event.transform)
    }
    /*
    tickActions() {
        //update circle positions each tick of the simulation
        let circle = this.circleG.selectAll('circle').data(this.nodes, d=>d.id)
            .enter().append('circle')
            .attr('r', this.nodeRadius)
            .attr('stroke-width', 0.5)
            .attr('stroke', 'white')
            .attr('fill', 'red')
            .attr('cx', d=>d.x)
            .attr('cy', d=>d.y);

        circle.transition().duration(1) //1000
            .attr('cx', d=>d.x)
            .attr('cy', d=>d.y)
            .attr('id', d=>`node-${d.id}-`); 
        
            
        //update link positions 
        let path = this.pathG.selectAll('path').data(this.links, d=>d.id)
          .enter().append('path')
          //.attr('opacity', 1)
          .attr('opacity', o =>  (this.activeNode == o.target || this.activeNode == o.source || this.activeNode == null) ? 1 : 0.1 )
          .attr('stroke-linecap', 'round')
          .attr('stroke-width', '0.75px')
          .attr('fill', 'transparent');

        path.transition().duration(1) //1000
          .attr('id', d=>  `link-source-${d.source.id}-target-${d.target.id}-`)
          .attr('stroke', 'mediumblue')
          .attr("d", d => `M${d.source.x},${d.source.y}L${d.target.x},${d.target.y}`)
    }
    */

    fade(opacity, d) {
        this.activeNode = opacity === 0.1 ? d : null;
        const graph = this.graph
        this.circleG.selectAll('circle')
            .style('stroke-opacity', function (o) {
                const thisOpacity = graph.isConnected(d, o) ? 1 : opacity;
                this.setAttribute('fill-opacity', thisOpacity);
                //console.log(this, graph)
                if (!thisOpacity) console.log(o)
                return thisOpacity;
            });
        this.pathG.selectAll('path')
            .style('stroke-opacity', o => (o.source === d || o.target === d ? 1 : opacity) );
    };

}


function createGraph() {
    const nodes = d3.range(0,20).map( d=> ({id:d, fx:50+ ~~(Math.random()*d*25), fy:50+~~(Math.random()*d*25)}) );
    const links = d3.range(0,25).map( d=> ({id: d, source: ~~(Math.random()*20), target: ~~(Math.random()*20)}) )
    return new Graph(nodes, links)
}


let view, slider;
const morph = function(){
    const g = createGraph()
    view.update(g)
}

const loadNetworks = function(){
    const networks = [];
    for (let i=0; i<30; i++){
        const g = createGraph();
        networks.push(g)
    }
    return networks;
}

window.onload = () => {
    new SourceSelector();
    //const networks = loadNetworks();
    //slider = new TemporalSlider(networks);
    //view = new NetworkViewer();
    //const buttton = document.getElementById('morph');
    //buttton.addEventListener('click', morph);
}



////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////
//reference:  https://jsfiddle.net/bfbun6cc/4/
//reference: https://stackoverflow.com/questions/34934577/html-range-slider-with-play-pause-loop

class TemporalSlider{
    constructor(networks=[]){
        this.start = 0;
        this.end = networks.length-1;
        this.current = 0;
        this.networks = networks;
        this.view = new NetworkViewer();
        this.addHTMLInputs();
        this.updateView();
    }
    addHTMLInputs(){
        const container = document.getElementById('slider');
        container.innerHTML = "" +
        `<input type='number' min='${this.start}' max='${this.end}' id='rangeText' value=${this.start} disabled></output>   
        <input type='range' min='${this.start}' max='${this.end}' step='1' value='${this.current}' id='rangeSlider' onkeydown="return false;"/> 
        <button type="button" name="play" id="play" class="btn play"><i class="fa fa-play"></i></button>`
        this.slider = document.getElementById('rangeSlider');
        this.button = document.getElementById('play');
        this.timefield = document.getElementById('rangeText');
        this.addRenderEvents();
    }
    addRenderEvents(){
        this.slider.addEventListener('input', e => this.updateView() )
        this.button.addEventListener('click', e => this.toggleAnimation() )
        document.body.addEventListener('keydown', e => this.moveOnKeyUp(e) );
        this.time = Date.now()
        this.now = 0;
        this.playtimer;
    }
    updateView(){
        this.timefield.value = this.slider.value;
        const index = this.slider.value;
        const graph = this.networks[index];
        this.view.update(graph)     
    }
    toggleAnimation(){
        if (this.button.name === 'play'){
                this.button.name = 'pause'
                this.button.className = "pause btn"
                this.button.innerHTML = `<i class="fa fa-pause"></i>` //Pause
                this.play();
                this.playtimer = setInterval( () => this.play(), this.view.duration ); //1000
        }
        else{
            this.button.name = 'play';
            this.button.className = "play btn"
            this.button.innerHTML =  `<i class="fa fa-play"></i>` //Play
            clearInterval(this.playtimer);

        }
    }
    moveOnKeyUp(e){
        this.now = Date.now()
        if (this.now - this.time > 200 ){
            if (e.keyCode == 39){
                this.slider.value = (this.slider.value < this.end) ? +this.slider.value + 1 : this.end;
                this.updateView();
            }
            if (e.keyCode == 37){
                this.slider.value = (this.slider.value > 0 ) ? +this.slider.value - 1 : 0; 
                this.updateView();
            }
            this.time = Date.now()
        }
    }
    play(){
        this.slider.value = (+this.slider.value + 1) % (this.end+1);
        this.updateView();
    }
}

class FolderLoader{
    constructor(containerID ='source-input', ext='.json'){
        document.getElementById(containerID).innerHTML = "" +
        `<input id="folder-uploader" type="file" name='file' webkitdirectory directory multiple>`
        this.folderUpload = document.getElementById('folder-uploader');
        this.folderUpload.addEventListener('change', () => this.getFiles(ext) )
    }
    async getFiles( ...extensions){
        const data = [];
        //let files = this.folderUpload.files;                                                                   //v1: ets all files
        //let files = [ ...this.folderUpload.files].filter(f=>f.name.includes(ext))                              //v2: apply filter for one extension
        extensions = extensions.length ? extensions : ['']                                                       //v3: apply filter on n extensions
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
         //console.log(networks)
         //networks = [createGraph()]
         //console.log(networks)
         slider = new TemporalSlider(networks);
         test = slider;
    }

}

var test


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
            case 'github': new GithubLoader(); break;
            default: 
            const tnet = await eel.get_tnet(this.selector.value)()
            new AppLoader(tnet); break;
            //new AppLoader(this.selector.value); break;
        }
    }
}


const selector = document.getElementById('location-selector')
//selector.addEventListener( "change", updateSelector)
async function updateSelector(){
    const selector = document.getElementById('location-selector')
    selector.innerHTML = ""
    selector.innerHTML += `<option default value='local'>Local</option>`
    selector.innerHTML += `<option value='github'>Github</option>`
    count = await eel.get_count()()
    console.log("tnet_count",count)
    for (let i=1; i<=count; i++){
        const label = await eel.get_description(i)();
        selector.innerHTML += `<option value='${i}'>${i}:${label}</option>`
    }
}
updateSelector()


class AppLoader{
    constructor(tnet){
        console.log(tnet)
        const data = [];
        for (let g of tnet){
            const json = JSON.parse(g)
            data.push(json);
        }
    this.load(data)
    }
    load(data){
        //separate out this function
        let networks = data.map( item => new Graph(item.nodes, item.links))
        //console.log(networks)
        //networks = [createGraph()]
        //console.log(networks)
        slider = new TemporalSlider(networks);
        test = slider;
    }
}



class GithubLoader{
    constructor(containerID ='source-input', ext='json'){
        document.getElementById(containerID).innerHTML = "" +
        `<form id='github-form' style='display:inline;' onSubmit="return false;">
        <button id='github-button'>Import Files</button>
        <input id="github-uploader" type="url" placeholder="https://github.com/user/repo/tree/branch/path/to/data" 
            required pattern="https:\/\/github.com\/.*\/.*\/tree\/([^\/;]+)\/.*" style="width:300px;"
        >
        </form>`
        this.url = document.getElementById('github-uploader');
        //const urlButton = document.getElementById('github-button');
        //urlButton.addEventListener('', () => this.getFiles())
        const githubForm = document.getElementById('github-form');
        githubForm.addEventListener('submit', ()=>this.getFiles(ext) );
        
    }
    /*
    async getFiles(ext='json'){
            const regex = /https:\/\/github.com\/(?<user>.*)\/(?<repo>.*)\/tree\/([^\/;]+)\/(?<path>.*)/
            let {groups: {user, repo, path}} = regex.exec(this.url.value);

            //Test for filtering by path JSON data
            this.data = []
            const responseGETFileList = await fetch(`https://api.github.com/search/code?q=path:${path}+extension:${ext}+repo:${user}/${repo}`) 
            const fileList = await responseGETFileList.json()
            for (let item of fileList.items ){
                const responseGETFile = await fetch(item.git_url)
                const blobData = await responseGETFile.json()
                const jsonString = atob(blobData.content)
                const json = JSON.parse(jsonString)
                this.data.push(json)
            } 
            slider = new TemporalSlider(this.data);
       return false;
    }*/
    async getFiles(ext){
        const regex = /https:\/\/github.com\/(?<user>.*)\/(?<repo>.*)\/tree\/([^\/;]+)\/(?<path>.*)/
        const {groups: {user, repo, path}} = regex.exec(this.url.value);
        const fileList = await this.loadFilesList(user, repo, path,ext);
        const data = []
        for (let item of fileList.items){
            try {
                const json = await this.getGitURL(item.git_url);
                data.push(json)
            }
            catch{
                const json = await this.getRawGit(user,repo, item.path);
                data.push(json)
            }
        }
        this.load(data)

    }
    async loadFilesList(user, repo, path,ext){
        if (!localStorage.getItem(user+repo+path+ext)){
            const fileList = await this.requestFilesList(user,repo,path,ext);
            localStorage.setItem(user+repo+path+ext, JSON.stringify(fileList));
        }
        return JSON.parse(localStorage.getItem(user+repo+path+ext)); 
    }
    async requestFilesList(user,repo,path,ext='json'){
        const responseGETFileList = await fetch(`https://api.github.com/search/code?q=path:${path}+extension:${ext}+repo:${user}/${repo}`) 
        const fileList = await responseGETFileList.json()
        return fileList;
    }
    async getGitURL(gitURL){
        const responseGETFile = await fetch(gitURL)
        const blobData = await responseGETFile.json()
        const jsonString = atob(blobData.content)
        const json = JSON.parse(jsonString)
        return json
    }
    async getRawGit(user,repo,path){
        const url = `https://raw.githack.com/${user}/${repo}/master/${path}`
        const responseGETFile = await fetch(url)
        const jsonData = await responseGETFile.json()
        return jsonData;
        //const jsonString = atob(blobData.content)
        //const json = JSON.parse(jsonString)
        //this.data.push(json)
    }
    load(data){
        //separate out this function
        let networks = data.map( item => new Graph(item.nodes, item.links))
        //console.log(networks)
        //networks = [createGraph()]
        //console.log(networks)
        slider = new TemporalSlider(networks);
        test = slider;
   }
}


//<input type='button' id='github-button' value=' Import  Files'>


//references:
//Get folder of files uploaded into browser
//https://stackoverflow.com/questions/43958335/select-folder-instead-of-single-file-input

// Filtering N-extensions: (Use some for array of extensions)
//https://stackoverflow.com/questions/37896484/multiple-conditions-for-javascript-includes-method
