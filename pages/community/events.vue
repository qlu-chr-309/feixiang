<template>
	<view class="events-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">赛事信息</view>
		</view>
		
		<view class="tabs">
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'upcoming' }" 
				@click="switchTab('upcoming')"
			>
				即将开始
			</view>
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'ongoing' }" 
				@click="switchTab('ongoing')"
			>
				正在进行
			</view>
			<view 
				class="tab-item" 
				:class="{ active: activeTab === 'past' }" 
				@click="switchTab('past')"
			>
				往期回顾
			</view>
		</view>
		
		<view class="search-bar">
			<view class="search-input">
				<text class="iconfont icon-search"></text>
				<input type="text" placeholder="搜索赛事" confirm-type="search" v-model="searchText" @confirm="search" />
			</view>
			<view class="filter-btn" @click="showFilter">
				<text class="iconfont icon-filter"></text>
			</view>
		</view>
		
		<view class="content-list">
			<view class="event-item" v-for="(item, index) in filteredEvents" :key="index" @click="viewEventDetail(item)">
				<image :src="item.image" mode="aspectFill" class="event-image"></image>
				<view class="event-content">
					<view class="event-status" :class="item.status">{{getStatusText(item.status)}}</view>
					<text class="event-title">{{item.title}}</text>
					<view class="event-info">
						<view class="info-item">
							<text class="iconfont icon-time"></text>
							<text>{{item.time}}</text>
						</view>
						<view class="info-item">
							<text class="iconfont icon-location"></text>
							<text>{{item.location}}</text>
						</view>
					</view>
					<view class="event-stats">
						<text class="participant-count">{{item.participants}}人报名</text>
						<text class="event-tag" v-for="(tag, tagIndex) in item.tags" :key="tagIndex">{{tag}}</text>
					</view>
					<view class="event-action">
						<button 
							class="action-btn" 
							:class="item.status === 'upcoming' ? 'primary' : 'default'"
							@click.stop="actionEvent(item)"
						>
							{{getActionText(item.status)}}
						</button>
					</view>
				</view>
			</view>
			
			<view class="empty-state" v-if="filteredEvents.length === 0">
				<image src="/static/community/empty-events.png" class="empty-image"></image>
				<text class="empty-text">暂无{{getTabText(activeTab)}}赛事</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				activeTab: 'upcoming',
				searchText: '',
				events: [
					{
						id: 1,
						title: '2023年全国无人机创新应用大赛',
						time: '2023-05-20 ~ 2023-05-22',
						location: '深圳市南山区科技园',
						status: 'upcoming',
						image: '/static/community/event1.jpg',
						participants: 356,
						tags: ['创新应用', '全国赛']
					},
					{
						id: 2,
						title: '无人机航拍技能挑战赛',
						time: '2023-05-15 ~ 2023-05-18',
						location: '上海市浦东新区外滩',
						status: 'upcoming',
						image: '/static/community/event2.jpg',
						participants: 128,
						tags: ['航拍', '技能挑战']
					},
					{
						id: 3,
						title: '第三届无人机竞速挑战赛',
						time: '2023-04-28 ~ 2023-05-05',
						location: '北京市朝阳区奥林匹克公园',
						status: 'ongoing',
						image: '/static/community/event3.jpg',
						participants: 205,
						tags: ['竞速', '挑战赛']
					},
					{
						id: 4,
						title: '无人机创客马拉松',
						time: '2023-04-25 ~ 2023-04-27',
						location: '广州市天河区软件园',
						status: 'ongoing',
						image: '/static/community/event4.jpg',
						participants: 76,
						tags: ['创客', '马拉松']
					},
					{
						id: 5,
						title: '2023春季无人机编程大赛',
						time: '2023-03-15 ~ 2023-03-20',
						location: '成都市高新区天府软件园',
						status: 'past',
						image: '/static/community/event5.jpg',
						participants: 189,
						tags: ['编程', '开发者']
					},
					{
						id: 6,
						title: '无人机应用创新展示会',
						time: '2023-02-10 ~ 2023-02-12',
						location: '杭州市西湖区云栖小镇',
						status: 'past',
						image: '/static/community/event6.jpg',
						participants: 325,
						tags: ['应用创新', '展示会']
					}
				]
			}
		},
		computed: {
			filteredEvents() {
				let result = this.events.filter(item => item.status === this.activeTab);
				
				if (this.searchText) {
					const searchLower = this.searchText.toLowerCase();
					result = result.filter(item => 
						item.title.toLowerCase().includes(searchLower) || 
						item.location.toLowerCase().includes(searchLower) ||
						item.tags.some(tag => tag.toLowerCase().includes(searchLower))
					);
				}
				
				return result;
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			switchTab(tab) {
				this.activeTab = tab;
			},
			getTabText(tab) {
				const tabTexts = {
					'upcoming': '即将开始',
					'ongoing': '正在进行',
					'past': '往期'
				};
				return tabTexts[tab] || '';
			},
			getStatusText(status) {
				const statusTexts = {
					'upcoming': '即将开始',
					'ongoing': '进行中',
					'past': '已结束'
				};
				return statusTexts[status] || '';
			},
			getActionText(status) {
				const actionTexts = {
					'upcoming': '立即报名',
					'ongoing': '查看详情',
					'past': '查看回顾'
				};
				return actionTexts[status] || '';
			},
			search() {
				// 已通过计算属性实现
				uni.showToast({
					title: '搜索: ' + this.searchText,
					icon: 'none'
				});
			},
			showFilter() {
				uni.showToast({
					title: '筛选功能正在开发中',
					icon: 'none'
				});
			},
			viewEventDetail(event) {
				uni.navigateTo({
					url: '/pages/community/eventDetail?id=' + event.id
				});
			},
			actionEvent(event) {
				if (event.status === 'upcoming') {
					uni.navigateTo({
						url: '/pages/community/eventRegister?id=' + event.id
					});
				} else {
					this.viewEventDetail(event);
				}
			}
		}
	}
</script>

<style>
	.events-container {
		min-height: 100vh;
		background-color: #f5f5f5;
	}
	
	.header {
		background-color: #007AFF;
		padding: 20rpx 30rpx;
		color: #fff;
		display: flex;
		align-items: center;
		position: relative;
	}
	
	.back-btn {
		position: absolute;
		left: 30rpx;
	}
	
	.header-title {
		flex: 1;
		font-size: 36rpx;
		font-weight: bold;
		text-align: center;
	}
	
	.tabs {
		display: flex;
		background-color: #fff;
		border-bottom: 1rpx solid #eee;
		position: sticky;
		top: 0;
		z-index: 10;
	}
	
	.tab-item {
		flex: 1;
		text-align: center;
		padding: 24rpx 0;
		font-size: 28rpx;
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
		height: 6rpx;
		background-color: #007AFF;
		border-radius: 3rpx;
	}
	
	.search-bar {
		display: flex;
		padding: 20rpx;
		background-color: #fff;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.search-input {
		flex: 1;
		display: flex;
		align-items: center;
		background-color: #f5f5f5;
		border-radius: 30rpx;
		padding: 10rpx 20rpx;
		margin-right: 20rpx;
	}
	
	.search-input .iconfont {
		color: #999;
		font-size: 32rpx;
		margin-right: 10rpx;
	}
	
	.search-input input {
		flex: 1;
		height: 60rpx;
		font-size: 28rpx;
	}
	
	.filter-btn {
		width: 80rpx;
		height: 80rpx;
		background-color: #f5f5f5;
		border-radius: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.filter-btn .iconfont {
		color: #666;
		font-size: 36rpx;
	}
	
	.content-list {
		padding: 20rpx;
	}
	
	.event-item {
		background-color: #fff;
		border-radius: 12rpx;
		margin-bottom: 20rpx;
		overflow: hidden;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	
	.event-image {
		width: 100%;
		height: 300rpx;
	}
	
	.event-content {
		padding: 24rpx;
		position: relative;
	}
	
	.event-status {
		position: absolute;
		top: -40rpx;
		right: 24rpx;
		height: 60rpx;
		padding: 0 30rpx;
		background-color: #1890ff;
		color: #fff;
		font-size: 26rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 30rpx;
	}
	
	.event-status.upcoming {
		background-color: #1890ff;
	}
	
	.event-status.ongoing {
		background-color: #52c41a;
	}
	
	.event-status.past {
		background-color: #d9d9d9;
	}
	
	.event-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 16rpx;
		display: block;
	}
	
	.event-info {
		margin-bottom: 16rpx;
	}
	
	.info-item {
		display: flex;
		align-items: center;
		margin-bottom: 10rpx;
		font-size: 26rpx;
		color: #666;
	}
	
	.info-item .iconfont {
		margin-right: 10rpx;
		color: #999;
	}
	
	.event-stats {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		margin-bottom: 16rpx;
	}
	
	.participant-count {
		font-size: 24rpx;
		color: #ff4d4f;
		margin-right: 16rpx;
	}
	
	.event-tag {
		font-size: 24rpx;
		color: #1890ff;
		background-color: #e6f7ff;
		padding: 6rpx 16rpx;
		border-radius: 30rpx;
		margin-right: 10rpx;
		margin-bottom: 10rpx;
	}
	
	.event-action {
		text-align: right;
	}
	
	.action-btn {
		display: inline-block;
		font-size: 28rpx;
		padding: 12rpx 40rpx;
		border-radius: 40rpx;
		border: none;
	}
	
	.action-btn.primary {
		background-color: #007AFF;
		color: #fff;
	}
	
	.action-btn.default {
		background-color: #f5f5f5;
		color: #666;
	}
	
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
		margin-bottom: 30rpx;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
</style> 