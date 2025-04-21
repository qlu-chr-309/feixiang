<template>
	<view class="demand-container">
		<view class="header">
			<view class="tabs">
				<view class="tab-item" :class="{ active: activeTab === 'my' }" @click="switchTab('my')">
					<text>我的需求</text>
				</view>
				<view class="tab-item" :class="{ active: activeTab === 'all' }" @click="switchTab('all')">
					<text>全部需求</text>
				</view>
			</view>
		</view>
		
		<view class="content">
			<view v-if="activeTab === 'my'">
				<view class="empty-tip" v-if="myDemands.length === 0">
					<image src="/static/empty.png" mode="aspectFit" class="empty-image"></image>
					<text>您还没有发布过需求</text>
					<button class="publish-btn" @click="navigateToPublish">发布需求</button>
				</view>
				
				<view class="demand-list" v-else>
					<view class="demand-item" v-for="(item, index) in myDemands" :key="index" @click="viewDetail(item.id)">
						<view class="demand-title">{{item.title}}</view>
						<view class="demand-desc">{{item.description}}</view>
						<view class="demand-footer">
							<view class="demand-price">¥{{item.budget}}</view>
							<view class="demand-status" :class="'status-' + item.status">{{statusText[item.status]}}</view>
						</view>
					</view>
				</view>
			</view>
			
			<view v-if="activeTab === 'all'">
				<view class="filter-bar">
					<view class="filter-item" :class="{ active: currentFilter === 'all' }" @click="setFilter('all')">
						<text>全部</text>
					</view>
					<view class="filter-item" :class="{ active: currentFilter === 'aerial' }" @click="setFilter('aerial')">
						<text>航拍</text>
					</view>
					<view class="filter-item" :class="{ active: currentFilter === 'plant' }" @click="setFilter('plant')">
						<text>植保</text>
					</view>
					<view class="filter-item" :class="{ active: currentFilter === 'inspection' }" @click="setFilter('inspection')">
						<text>巡检</text>
					</view>
				</view>
				
				<view class="demand-list">
					<view class="demand-item" v-for="(item, index) in filteredDemands" :key="index" @click="viewDetail(item.id)">
						<view class="demand-title">{{item.title}}</view>
						<view class="demand-desc">{{item.description}}</view>
						<view class="demand-footer">
							<view class="demand-price">¥{{item.budget}}</view>
							<view class="demand-date">{{item.date}}</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view class="float-btn" @click="navigateToPublish">
			<text class="btn-text">发布需求</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				activeTab: 'all',
				currentFilter: 'all',
				statusText: {
					'pending': '待响应',
					'inprogress': '进行中',
					'completed': '已完成',
					'cancelled': '已取消'
				},
				myDemands: [
					// 示例数据，实际应从API获取
					{ id: 1, title: '农田植保服务', description: '需要对100亩水稻进行无人机喷洒农药服务', budget: '3000', status: 'pending' },
					{ id: 2, title: '建筑工地航拍', description: '需要对建筑工地进行航拍，记录工程进度', budget: '1500', status: 'inprogress' }
				],
				allDemands: [
					{ id: 1, title: '农田植保作业', description: '100亩小麦农田需要喷洒农药，地点在河南周口', budget: '2000', date: '2023-04-10', type: 'plant' },
					{ id: 2, title: '城市建筑航拍', description: '需要专业航拍团队拍摄城市建筑宣传片，时长5分钟', budget: '5000', date: '2023-04-09', type: 'aerial' },
					{ id: 3, title: '电力线路巡检', description: '50公里电力线路日常巡检，需要热成像设备', budget: '3000', date: '2023-04-08', type: 'inspection' },
					{ id: 4, title: '婚礼现场航拍', description: '需要航拍婚礼现场，时长3小时，含剪辑', budget: '2000', date: '2023-04-07', type: 'aerial' },
					{ id: 5, title: '果园植保作业', description: '30亩果园需要无人机喷洒农药，地点在陕西渭南', budget: '1500', date: '2023-04-06', type: 'plant' }
				]
			}
		},
		computed: {
			filteredDemands() {
				if (this.currentFilter === 'all') {
					return this.allDemands;
				} else {
					return this.allDemands.filter(item => item.type === this.currentFilter);
				}
			}
		},
		methods: {
			switchTab(tab) {
				this.activeTab = tab;
			},
			setFilter(filter) {
				this.currentFilter = filter;
			},
			viewDetail(id) {
				uni.navigateTo({
					url: '/pages/demand/detail?id=' + id
				});
			},
			navigateToPublish() {
				uni.navigateTo({
					url: '/pages/demand/publish'
				});
			}
		}
	}
</script>

<style>
	.demand-container {
		min-height: 100vh;
		background-color: #f5f5f5;
		position: relative;
		padding-bottom: 100rpx;
	}
	
	.header {
		background-color: #fff;
		border-bottom: 1rpx solid #eee;
	}
	
	.tabs {
		display: flex;
		height: 90rpx;
		line-height: 90rpx;
	}
	
	.tab-item {
		flex: 1;
		text-align: center;
		font-size: 30rpx;
		color: #666;
		position: relative;
	}
	
	.tab-item.active {
		color: #007AFF;
		font-weight: bold;
	}
	
	.tab-item.active::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 50%;
		transform: translateX(-50%);
		width: 60rpx;
		height: 4rpx;
		background-color: #007AFF;
	}
	
	.content {
		padding: 20rpx;
	}
	
	.filter-bar {
		display: flex;
		background-color: #fff;
		padding: 20rpx;
		border-radius: 10rpx;
		margin-bottom: 20rpx;
	}
	
	.filter-item {
		padding: 10rpx 20rpx;
		margin-right: 20rpx;
		font-size: 26rpx;
		color: #666;
		border-radius: 30rpx;
		background-color: #f5f5f5;
	}
	
	.filter-item.active {
		background-color: #007AFF;
		color: #fff;
	}
	
	.demand-list {
		display: flex;
		flex-direction: column;
	}
	
	.demand-item {
		background-color: #fff;
		padding: 30rpx;
		border-radius: 10rpx;
		margin-bottom: 20rpx;
	}
	
	.demand-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.demand-desc {
		font-size: 28rpx;
		color: #666;
		margin-bottom: 20rpx;
	}
	
	.demand-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.demand-price {
		font-size: 28rpx;
		color: #ff6600;
		font-weight: bold;
	}
	
	.demand-date, .demand-status {
		font-size: 26rpx;
		color: #999;
	}
	
	.status-pending {
		color: #ff9900;
	}
	
	.status-inprogress {
		color: #007AFF;
	}
	
	.status-completed {
		color: #00cc00;
	}
	
	.status-cancelled {
		color: #999;
	}
	
	.empty-tip {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 100rpx 0;
	}
	
	.empty-image {
		width: 200rpx;
		height: 200rpx;
		margin-bottom: 30rpx;
	}
	
	.publish-btn {
		margin-top: 30rpx;
		background-color: #007AFF;
		color: #fff;
		padding: 20rpx 40rpx;
		border-radius: 40rpx;
		font-size: 28rpx;
	}
	
	.float-btn {
		position: fixed;
		bottom: 30rpx;
		right: 30rpx;
		width: 180rpx;
		height: 80rpx;
		border-radius: 40rpx;
		background-color: #007AFF;
		color: #fff;
		display: flex;
		justify-content: center;
		align-items: center;
		box-shadow: 0 6rpx 20rpx rgba(0, 122, 255, 0.3);
	}
	
	.btn-text {
		font-size: 28rpx;
	}
</style> 