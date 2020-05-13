const STORAGE_KEY = "mark"

export default{
    setItem(key, value){
        let val = this.getStorage();
        val[key] = value;
        window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(val))
    },
    getItem(key){
       return this.getStorage()[key];
    },
    getStorage(){
       return JSON.parse( window.sessionStorage.getItem(STORAGE_KEY) || '{}')
    },

}