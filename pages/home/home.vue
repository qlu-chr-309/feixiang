<template>
	<view class="home-container">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input">
				<text class="iconfont icon-search"></text>
				<input type="text" placeholder="搜索无人机服务、设备、供应商..." />
			</view>
		</view>
		
		<!-- 轮播图 -->
		<swiper class="banner" indicator-dots autoplay interval="3000" duration="500" circular>
			<swiper-item v-for="(item, index) in bannerList" :key="index">
				<image :src="item.image" mode="aspectFill"></image>
			</swiper-item>
		</swiper>
		
		<!-- 服务分类 -->
		<view class="section service-categories">
			<view class="category-item" v-for="(item, index) in categories" :key="index" @click="navigateTo(item.url)">
				<image :src="item.icon" mode="aspectFit" class="category-icon"></image>
				<text class="category-name">{{item.name}}</text>
			</view>
		</view>
		
		<!-- 热门需求 -->
		<view class="section">
			<view class="section-header">
				<text class="section-title">热门需求</text>
				<text class="more" @click="navigateTo('/pages/demand/demand')">查看更多 ></text>
			</view>
			<view class="demand-list">
				<view class="demand-item" v-for="(item, index) in demandList" :key="index" @click="viewDemandDetail(item.id)">
					<view class="demand-info">
						<text class="demand-title">{{item.title}}</text>
						<text class="demand-desc">{{item.description}}</text>
						<view class="demand-meta">
							<text class="demand-price">¥{{item.budget}}</text>
							<text class="demand-date">{{item.date}}</text>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 特色服务 -->
		<view class="section">
			<view class="section-header">
				<text class="section-title">特色服务</text>
				<text class="more" @click="navigateTo('/pages/service/service')">查看更多 ></text>
			</view>
			<view class="special-services">
				<view class="service-grid">
					<view class="service-grid-item" v-for="(item, index) in specialServices" :key="index" @click="navigateTo(item.url)">
						<image :src="item.image" mode="aspectFill" class="service-image"></image>
						<text class="service-title">{{item.title}}</text>
						<text class="service-desc">{{item.desc}}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 行业资讯 -->
		<view class="section">
			<view class="section-header">
				<text class="section-title">行业资讯</text>
				<text class="more">查看更多 ></text>
			</view>
			<view class="news-list">
				<view class="news-item" v-for="(item, index) in newsList" :key="index">
					<image :src="item.image" mode="aspectFill" class="news-image"></image>
					<view class="news-info">
						<text class="news-title">{{item.title}}</text>
						<text class="news-date">{{item.date}}</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				bannerList: [
					{ image: '../../static/banner/banner1.png' },
					{ image: '../../static/banner/banner2.png' },
					{ image: '../../static/banner/banner3.png' }
				],
				categories: [
					{ name: '无人机采购', icon: '../../static/icon/purchase.png', url: '/pages/service/purchase' },
					{ name: '飞行服务', icon: '../../static/icon/flight.png', url: '/pages/service/flight' },
					{ name: '植保作业', icon: '../../static/icon/plant.png', url: '/pages/service/plant' },
					{ name: '航拍摄影', icon: '../../static/icon/photo.png', url: '/pages/service/photo' },
					{ name: '配件更换', icon: '../../static/icon/parts.png', url: '/pages/service/parts' }
				],
				demandList: [
					{ id: 1, title: '农田植保作业', description: '100亩小麦农田需要喷洒农药，地点在河南周口', budget: '2000', date: '2023-04-10' },
					{ id: 2, title: '城市建筑航拍', description: '需要专业航拍团队拍摄城市建筑宣传片，时长5分钟', budget: '5000', date: '2023-04-09' },
					{ id: 3, title: '电力线路巡检', description: '50公里电力线路日常巡检，需要热成像设备', budget: '3000', date: '2023-04-08' }
				],
				specialServices: [
					{
						id: 1,
						title: '虚拟飞行体验',
						desc: '足不出户体验飞行乐趣',
						image: '../../static/service/virtual.png',
						url: '/pages/service/virtual'
					},
					{
						id: 2,
						title: '无人机竞速赛',
						desc: '体验速度与激情',
						image: '../../static/service/competition.png',
						url: '/pages/service/competition'
					},
					{
						id: 3,
						title: '创客实验室',
						desc: '自己动手组装无人机',
						image: '../../static/service/maker.png',
						url: '/pages/service/maker'
					},
					{
						id: 4,
						title: '飞行技能培训',
						desc: '专业的飞行技能培训',
						image: '../../static/service/training.png',
						url: '/pages/service/training'
					}
				],
				newsList: [
					{ id: 1, title: '最新民航局无人机管理条例解读', image: '../../static/news/n1.png', date: '2023-04-10' },
					{ id: 2, title: '2023年无人机行业发展趋势分析', image: '../../static/news/n2.png', date: '2023-04-08' },
					{ id: 3, title: '大疆发布新一代农业植保无人机', image: '../../static/news/n3.png', date: '2023-04-06' }
				]
			}
		},
		onShow() {
			// uni-app不需要设置tabbar selected
			// 但可以在这里加载数据
		},
		methods: {
			navigateTo(url) {
				uni.navigateTo({
					url: url
				})
			},
			viewDemandDetail(id) {
				uni.navigateTo({
					url: '/pages/demand/detail?id=' + id
				});
			},
			viewNewsDetail(id) {
				uni.showToast({
					title: '资讯详情功能开发中',
					icon: 'none'
				});
			}
		}
	}
</script>

<style>
	.home-container {
		padding-bottom: 30rpx;
		background-color: #f5f5f5;
	}
	
	.search-bar {
		padding: 20rpx 30rpx;
		background-color: #007AFF;
	}
	
	.search-input {
		display: flex;
		align-items: center;
		background-color: #fff;
		height: 70rpx;
		border-radius: 35rpx;
		padding: 0 30rpx;
	}
	
	.icon-search {
		margin-right: 10rpx;
		color: #999;
	}
	
	.banner {
		width: 100%;
		height: 360rpx;
	}
	
	.banner image {
		width: 100%;
		height: 100%;
	}
	
	.section {
		background-color: #fff;
		margin: 20rpx 0;
		padding: 30rpx;
		border-radius: 12rpx;
	}
	
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
	
	.more {
		font-size: 24rpx;
		color: #007AFF;
	}
	
	.service-categories {
		display: flex;
		justify-content: space-between;
		flex-wrap: wrap;
	}
	
	.category-item {
		width: 20%;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 10rpx 0;
	}
	
	.category-icon {
		width: 80rpx;
		height: 80rpx;
		margin-bottom: 10rpx;
	}
	
	.category-name {
		font-size: 24rpx;
		color: #333;
	}
	
	.demand-list {
		display: flex;
		flex-direction: column;
	}
	
	.demand-item {
		padding: 20rpx 0;
		border-bottom: 1rpx solid #eee;
	}
	
	.demand-item:last-child {
		border-bottom: none;
	}
	
	.demand-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.demand-desc {
		font-size: 24rpx;
		color: #666;
		margin-bottom: 10rpx;
	}
	
	.demand-meta {
		display: flex;
		justify-content: space-between;
	}
	
	.demand-price {
		font-size: 24rpx;
		color: #e74c3c;
		font-weight: bold;
	}
	
	.demand-date {
		font-size: 24rpx;
		color: #999;
	}
	
	.service-grid {
		display: flex;
		flex-wrap: wrap;
		margin: 0 -10rpx;
	}
	
	.service-grid-item {
		width: 50%;
		padding: 10rpx;
		box-sizing: border-box;
	}
	
	.service-image {
		width: 100%;
		height: 200rpx;
		border-radius: 8rpx;
		margin-bottom: 10rpx;
	}
	
	.service-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 5rpx;
	}
	
	.service-desc {
		font-size: 24rpx;
		color: #666;
	}
	
	.news-list {
		display: flex;
		flex-direction: column;
	}
	
	.news-item {
		display: flex;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #eee;
	}
	
	.news-item:last-child {
		border-bottom: none;
	}
	
	.news-image {
		width: 180rpx;
		height: 120rpx;
		border-radius: 8rpx;
		margin-right: 20rpx;
	}
	
	.news-info {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
	
	.news-title {
		font-size: 28rpx;
		color: #333;
	}
	
	.news-date {
		font-size: 24rpx;
		color: #999;
	}
</style> 