Component({
  properties: {
    selected: {
      type: Number,
      value: 0
    }
  },
  
  data: {
    color: "#7A7E83",
    selectedColor: "#007AFF",
    list: [
      {
        pagePath: "/pages/home/home",
        iconPath: "../../static/images/tabbar/location.png",
        selectedIconPath: "../../static/images/tabbar/location.png",
        text: "首页"
      },
      {
        pagePath: "/pages/demand/demand",
        iconPath: "../../static/images/tabbar/smile.png",
        selectedIconPath: "../../static/images/tabbar/smile.png",
        text: "需求"
      },
      {
        pagePath: "/pages/service/service",
        iconPath: "../../static/images/tabbar/briefcase.png",
        selectedIconPath: "../../static/images/tabbar/briefcase.png",
        text: "服务"
      },
      {
        pagePath: "/pages/community/community",
        iconPath: "../../static/images/tabbar/chat.png",
        selectedIconPath: "../../static/images/tabbar/chat.png",
        text: "社区"
      },
      {
        pagePath: "/pages/my/my",
        iconPath: "../../static/images/tabbar/store.png",
        selectedIconPath: "../../static/images/tabbar/store.png",
        text: "我的"
      }
    ]
  },
  
  methods: {
    switchTab(e) {
      const data = e.currentTarget.dataset;
      const url = data.path;
      wx.switchTab({ url });
    }
  }
}) 