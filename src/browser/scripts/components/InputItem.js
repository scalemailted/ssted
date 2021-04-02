class InputItem{
    constructor(label, id, value,parent='input-div'){
        this.html = document.getElementById(parent);
        this.label = label;
        this.id = id;
        this.value = value;
        this.render();
    }
    render(){
        this.html.innerHTML +=  
        `<div class="form-group row">
            <label for="${this.id}" class="text-right col-md-6 col-form-label">${this.label}</label>
            <div class="col-md-6">
                <input id="${this.id}" class="form-control" value='${this.value}'>
            </div>
        </div>`
    }
}

class SelectorItem{
    constructor(label, id, parent, ...options){
        this.html = document.getElementById(parent);
        this.label = label;
        this.id = id;
        this.options = options;
        this.render();
    }
    render(){
        this.html.innerHTML +=
        `<div class="form-group row">
            <label for="${this.id}"" class="text-right col-md-6 col-form-label">${this.label}</label>
            <div class="col-md-6">
                <select id="${this.id}" class="form-control">
                    ${ this.getOptions() }
                </select>
            </div>
        </div> `
    }
    getOptions(){
        let htmlOptions = '';
        for (let option of this.options ){
            htmlOptions += `<option>${option}</option>`
        }
        return htmlOptions
    }
}



