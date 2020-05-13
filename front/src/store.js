import Vue from 'vue'
import vuex from 'vuex'

Vue.use(vuex)

export default new vuex.Store({
    state:{
        data: undefined ,
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