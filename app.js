// app.js
App({
  onLaunch: function() {
    console.log('App Launch');
    // 兼容uni-app
    if (typeof uni !== 'undefined') {
      console.log('使用uni-app框架');
    }
  },
  onShow: function() {
    console.log('App Show');
  },
  onHide: function() {
    console.log('App Hide');
  },
  globalData: {
    userInfo: null,
    isLoggedIn: false,
    userRole: '' // 'buyer' or 'supplier'
  }
}) 