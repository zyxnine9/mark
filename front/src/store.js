import Vue from 'vue'
import vuex from 'vuex'
import {data} from './assets/data'

Vue.use(vuex)

export default new vuex.Store({
    state:{
        data: data ,
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