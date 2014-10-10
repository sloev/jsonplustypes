
Date.prototype.old_toJSON = Date.prototype.toJSON
Date.prototype.toJSON = function(){
    return {"__TYPE__":"DATETIME", "__VALUE__":this.getTime()};
};

var dateStringify = function (key, value){
    if (typeof(value) === "object"){
        if ("__TYPE__" in value && "__VALUE__" in value){
            if (value["__TYPE__"]=== "DATETIME"){
                d = new Date();
                d.setTime(value["__VALUE__"]);
                return d;
            }
        }
    }
    return value;
};


//usage:
//
var in_data = {
  "date" : new Date()
};
var json_string = JSON.stringify(in_data);
var out_data = JSON.parse(json_string, dateStringify);
var equals = in_data['date'].getTime() === out_data['date'].getTime();
console.log("in:",in_data);
console.log("json string:", json_string);
console.log("out",out_data);
console.log("equal:", equals);

