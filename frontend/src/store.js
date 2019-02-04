import Vue from 'vue'
import Vuex from 'vuex'
import qs from 'qs'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        LoggedIn: false, 
        token: "default_token",
        user : ""
    },
    mutations: {
        //because vuex mutations are retarded and cant have 2 params
        login(state,payload) {
            state.token = payload.token
            state.user = payload.user
            state.LoggedIn = true
        },
        logout(state) {
            state.token = ''
            state.user = '' 
            state.LoggedIn = false
        }
    },
    actions: {
        login ({commit},creds) {
            return new Promise((resolve,reject) =>{
                Vue.axios.post('/login', qs.stringify(creds)).then(response => {
                    const token = response.data.token
                    const user = creds.username
                    localStorage.setItem('token', token)
                    localStorage.setItem('user', user)
                    commit("login",{token:token,user:user})
                    resolve(response)
                })
                    .catch( err => { reject(err)})

            })
        },
        logout ({commit}) {
            return new Promise((resolve) =>{
                Vue.axios.post('/logout').then(() => {
                    localStorage.removeItem('token')
                    localStorage.removeItem('user')
                    commit('logout')
                    resolve()
                })
            })
        }
    },
    getters: {
        user: state => state.user,
        token: state => state.token,
        LoggedIn: state => state.LoggedIn,
    } 
});




