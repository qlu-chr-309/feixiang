import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

// 全局状态管理
Vue.prototype.$store = {
  state: {
    userInfo: null,
    userType: '', // 'personal' 或 'enterprise'
    loginStatus: false,
    token: ''
  },
  setUserInfo(userInfo) {
    this.state.userInfo = userInfo
    this.state.loginStatus = true
  },
  setUserType(type) {
    this.state.userType = type
  },
  setToken(token) {
    this.state.token = token
    uni.setStorageSync('token', token)
  },
  logout() {
    this.state.userInfo = null
    this.state.loginStatus = false
    this.state.token = ''
    this.state.userType = ''
    uni.removeStorageSync('token')
    uni.removeStorageSync('userInfo')
  }
}

// 全局请求方法
Vue.prototype.$request = function(options) {
  const baseUrl = 'https://api.feixiang-app.com/v1' // 假设的API地址
  
  return new Promise((resolve, reject) => {
    uni.request({
      url: baseUrl + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + Vue.prototype.$store.state.token || ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // 未授权，需要重新登录
          Vue.prototype.$store.logout()
          uni.showToast({
            title: '登录已过期，请重新登录',
            icon: 'none'
          })
          uni.navigateTo({
            url: '/pages/login/login'
          })
          reject(res)
        } else {
          uni.showToast({
            title: res.data.message || '请求失败',
            icon: 'none'
          })
          reject(res)
        }
      },
      fail: (err) => {
        uni.showToast({
          title: '网络异常',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

App.mpType = 'app'

const app = new Vue({
  ...App
})
app.$mount() 