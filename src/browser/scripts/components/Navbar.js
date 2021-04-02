class Navbar{
    constructor(id, active){
        this.html = document.getElementById(id);
        this.id = id;
        this.active = active;
        this.render();        
    }
    render(){
        this.html.innerHTML = "" +
            `<nav class="navbar navbar-dark bg-dark py-0">
                <div class='navbar-expand container'>
                    <ul id='nav-list' class="nav navbar-nav nav-fill w-100"></ul>
                </div>
            </nav>`
        new NavItem('Home','main.html',this.active)
        new NavItem('Create','create.html',this.active)
        new NavItem('Analyze','analyze.html',this.active)
        new NavItem('Visualize','visualize.html',this.active)
        new NavItem('Documentation','documentation.html',this.active)
    }
}

class NavItem{
    constructor(name, href='#', active=''){
        this.html = document.getElementById('nav-list');
        this.name = name;
        this.href = href;
        this.active = active;
        this.render();
    }
    render(){
        console.log(this.name, this.active)
        this.html.innerHTML +=  
        `<li class="nav-item"> 
            <a href="${this.href}" ${this.active==this.name?'class="nav-link text-warning"':'class="nav-link"'}>
                ${this.name}
            </a> 
        </li>`
    }
}

/**
 * 
     <li class="nav-item">
        <a class="nav-link" href="main.html">Home</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">Create</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">Analyze</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="visualize.html">Visualize</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">Documentation</a>
    </li>


 */

