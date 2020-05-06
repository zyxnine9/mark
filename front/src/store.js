import Vue from 'vue'
import vuex from 'vuex'

Vue.use(vuex)

export default new vuex.Store({
    state:{
        data:[  [12,124,534,76575,324],
                [123,543,765,867123,12543,],
                [1232,32,68,123,456,8,6]],
    },
    actions:{
        setData(context, data){
            context.commit('SET_DATA', data)
        },      
    },
    mutations:{
        SET_DATA (state, data){
            state.data = data;
        },
    }
})