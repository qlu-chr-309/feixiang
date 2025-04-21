<template>
  <view class="news-container">
    <!-- 顶部分类 -->
    <view class="category-tabs">
      <view 
        class="tab-item" 
        :class="{ active: activeCategory === category.id }" 
        v-for="category in categories" 
        :key="category.id"
        @click="switchCategory(category.id)"
      >
        {{ category.name }}
      </view>
    </view>
    
    <!-- 新闻列表 -->
    <view class="news-list" v-if="newsList.length > 0">
      <!-- 置顶新闻 -->
      <view class="top-news" v-if="hasTopNews" @click="navigateToDetail(topNews.id)">
        <image class="top-image" :src="topNews.coverImage" mode="aspectFill"></image>
        <view class="top-overlay"></view>
        <view class="top-content">
          <view class="top-tag">置顶</view>
          <view class="top-title">{{ topNews.title }}</view>
          <view class="top-info">
            <text class="top-source">{{ topNews.source }}</text>
            <text class="top-time">{{ topNews.publishTime }}</text>
          </view>
        </view>
      </view>
      
      <!-- 普通新闻列表 -->
      <view class="news-item" v-for="(item, index) in normalNewsList" :key="index" @click="navigateToDetail(item.id)">
        <!-- 有图新闻 -->
        <view class="news-with-image" v-if="item.coverImage">
          <view class="news-content">
            <view class="news-title">{{ item.title }}</view>
            <view class="news-brief" v-if="item.brief">{{ item.brief }}</view>
            <view class="news-info">
              <text class="news-tag" v-if="item.tag">{{ item.tag }}</text>
              <text class="news-source">{{ item.source }}</text>
              <text class="news-time">{{ item.publishTime }}</text>
            </view>
          </view>
          <image class="news-image" :src="item.coverImage" mode="aspectFill"></image>
        </view>
        
        <!-- 无图新闻 -->
        <view class="news-without-image" v-else>
          <view class="news-title">{{ item.title }}</view>
          <view class="news-brief" v-if="item.brief">{{ item.brief }}</view>
          <view class="news-info">
            <text class="news-tag" v-if="item.tag">{{ item.tag }}</text>
            <text class="news-source">{{ item.source }}</text>
            <text class="news-time">{{ item.publishTime }}</text>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view class="load-more" v-if="hasMore" @click="loadMore">
        <text v-if="isLoading">加载中...</text>
        <text v-else>加载更多</text>
      </view>
      <view class="no-more" v-else>
        <text>没有更多了</text>
      </view>
    </view>
    
    <!-- 空状态 -->
    <view class="empty-state" v-else>
      <image class="empty-image" src="/static/images/empty-news.png" mode="aspectFit"></image>
      <text class="empty-text">暂无相关资讯</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 当前分类
      activeCategory: 'all',
      
      // 分类列表
      categories: [
        { id: 'all', name: '全部' },
        { id: 'policy', name: '政策法规' },
        { id: 'tech', name: '技术动态' },
        { id: 'market', name: '市场分析' },
        { id: 'enterprise', name: '企业动态' },
        { id: 'application', name: '应用案例' }
      ],
      
      // 新闻列表
      newsList: [
        {
          id: 1,
          title: '民航局发布最新无人机管理规定，对小型无人机飞行提出新要求',
          brief: '近日，中国民用航空局发布《无人驾驶航空器飞行管理规定》，提出了一系列新要求，涉及无人机飞行管理和运行安全保障等多方面内容。',
          source: '民航资源网',
          publishTime: '2小时前',
          tag: '政策法规',
          coverImage: '/static/images/news1.jpg',
          isTop: true
        },
        {
          id: 2,
          title: 'DJI发布最新农业植保无人机，效率提升30%',
          brief: '全球知名无人机制造商大疆创新推出最新一代农业植保无人机T50，单次作业效率较上一代产品提升30%。',
          source: '大疆创新',
          publishTime: '4小时前',
          tag: '技术动态',
          coverImage: '/static/images/news2.jpg'
        },
        {
          id: 3,
          title: '全国无人机飞行服务行业市场规模分析：到2025年将达到300亿元',
          brief: '据权威机构数据显示，中国无人机服务市场快速增长，预计2025年市场规模将达300亿元，复合增长率超过25%。',
          source: '无人机市场研究院',
          publishTime: '昨天',
          tag: '市场分析'
        },
        {
          id: 4,
          title: '浙江某电力公司采用无人机巡检，效率提升5倍',
          source: '电力资讯',
          publishTime: '2023-04-09',
          tag: '应用案例',
          coverImage: '/static/images/news3.jpg'
        },
        {
          id: 5,
          title: '多地出台无人机禁飞区域管理新规，特定区域需提前申请',
          source: '科技日报',
          publishTime: '2023-04-08',
          tag: '政策法规'
        }
      ],
      
      // 分页加载
      page: 1,
      pageSize: 10,
      hasMore: true,
      isLoading: false
    }
  },
  computed: {
    // 置顶新闻
    hasTopNews() {
      return this.newsList.some(item => item.isTop);
    },
    topNews() {
      return this.newsList.find(item => item.isTop) || {};
    },
    
    // 普通新闻列表（不包括置顶）
    normalNewsList() {
      return this.newsList.filter(item => !item.isTop);
    }
  },
  onLoad() {
    // 加载新闻列表
    this.loadNewsList();
  },
  methods: {
    // 切换分类
    switchCategory(categoryId) {
      if (this.activeCategory === categoryId) return;
      
      this.activeCategory = categoryId;
      
      // 重置列表和分页
      this.newsList = [];
      this.page = 1;
      this.hasMore = true;
      
      // 重新加载
      this.loadNewsList();
    },
    
    // 加载新闻列表
    loadNewsList() {
      // 模拟加载数据
      this.isLoading = true;
      
      setTimeout(() => {
        this.isLoading = false;
        
        // 实际应该调用接口获取数据
        // this.$request({
        //   url: '/news/list',
        //   method: 'GET',
        //   data: {
        //     category: this.activeCategory,
        //     page: this.page,
        //     pageSize: this.pageSize
        //   }
        // }).then(res => {
        //   if (this.page === 1) {
        //     this.newsList = res.data.list;
        //   } else {
        //     this.newsList = [...this.newsList, ...res.data.list];
        //   }
        //   this.hasMore = res.data.hasMore;
        // });
        
        // 模拟获取更多数据
        if (this.page > 1) {
          // 模拟加载更多数据
          const moreNews = [
            {
              id: 5 + this.page,
              title: '无人机在城市管理中的应用不断深入，智慧城市建设再添助力',
              source: '智慧城市观察',
              publishTime: '2023-04-0' + (7 - this.page),
              tag: '应用案例',
              coverImage: '/static/images/news4.jpg'
            }
          ];
          
          this.newsList = [...this.newsList, ...moreNews];
        }
        
        // 模拟数据加载完毕
        if (this.page >= 3) {
          this.hasMore = false;
        }
        
        this.page++;
      }, 1000);
    },
    
    // 加载更多
    loadMore() {
      if (this.isLoading || !this.hasMore) return;
      this.loadNewsList();
    },
    
    // 跳转到详情页
    navigateToDetail(id) {
      uni.navigateTo({
        url: `/pages/news/detail?id=${id}`
      });
    }
  },
  // 下拉刷新
  onPullDownRefresh() {
    // 重置列表和分页
    this.newsList = [];
    this.page = 1;
    this.hasMore = true;
    
    // 重新加载
    this.loadNewsList();
    
    setTimeout(() => {
      uni.stopPullDownRefresh();
    }, 1000);
  },
  // 触底加载更多
  onReachBottom() {
    if (this.hasMore && !this.isLoading) {
      this.loadMore();
    }
  }
}
</script>

<style>
.news-container {
  background-color: #f8f8f8;
  min-height: 100vh;
}

/* 分类标签 */
.category-tabs {
  display: flex;
  background-color: #fff;
  padding: 20rpx 0;
  white-space: nowrap;
  overflow-x: auto;
  position: sticky;
  top: 0;
  z-index: 100;
}

.tab-item {
  padding: 10rpx 30rpx;
  margin: 0 10rpx;
  font-size: 28rpx;
  color: #666;
  position: relative;
  display: inline-block;
}

.tab-item.active {
  color: #007AFF;
  font-weight: 500;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -6rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 30rpx;
  height: 4rpx;
  background-color: #007AFF;
  border-radius: 2rpx;
}

/* 新闻列表 */
.news-list {
  padding: 20rpx;
}

/* 置顶新闻 */
.top-news {
  position: relative;
  height: 360rpx;
  border-radius: 12rpx;
  overflow: hidden;
  margin-bottom: 30rpx;
}

.top-image {
  width: 100%;
  height: 100%;
}

.top-overlay {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 180rpx;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
}

.top-content {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 30rpx;
}

.top-tag {
  display: inline-block;
  font-size: 22rpx;
  color: #fff;
  background-color: #ff4500;
  padding: 6rpx 16rpx;
  border-radius: 4rpx;
  margin-bottom: 15rpx;
}

.top-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 15rpx;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.top-info {
  font-size: 24rpx;
  color: rgba(255,255,255,0.8);
}

.top-source {
  margin-right: 20rpx;
}

/* 普通新闻项 */
.news-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 6rpx rgba(0,0,0,0.05);
}

/* 有图新闻 */
.news-with-image {
  display: flex;
  justify-content: space-between;
}

.news-content {
  flex: 1;
  margin-right: 20rpx;
}

.news-title {
  font-size: 30rpx;
  font-weight: 500;
  color: #333;
  margin-bottom: 10rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-brief {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 20rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-info {
  font-size: 24rpx;
  color: #999;
}

.news-tag {
  display: inline-block;
  font-size: 22rpx;
  color: #007AFF;
  background-color: #e6f2ff;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
  margin-right: 15rpx;
}

.news-source {
  margin-right: 15rpx;
}

.news-image {
  width: 200rpx;
  height: 140rpx;
  border-radius: 8rpx;
}

/* 无图新闻 */
.news-without-image .news-title {
  margin-bottom: 15rpx;
}

/* 加载更多 */
.load-more, .no-more {
  text-align: center;
  padding: 30rpx 0;
  color: #999;
  font-size: 26rpx;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.empty-image {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}
</style> 