<template>
	<view class="event-detail-container">
		<view class="header">
			<view class="back-btn" @click="goBack">
				<text class="iconfont icon-back"></text>
			</view>
			<view class="header-title">赛事详情</view>
			<view class="share-btn">
				<text class="iconfont icon-share"></text>
			</view>
		</view>
		
		<view class="content-area">
			<image :src="eventData.image" mode="widthFix" class="event-banner"></image>
			
			<view class="event-header">
				<text class="event-title">{{eventData.title}}</text>
				<view class="event-status" :class="eventData.status">{{getStatusText(eventData.status)}}</view>
			</view>
			
			<view class="event-info-card">
				<view class="info-item">
					<text class="info-label">时间</text>
					<text class="info-value">{{eventData.time}}</text>
				</view>
				<view class="info-item">
					<text class="info-label">地点</text>
					<text class="info-value">{{eventData.location}}</text>
				</view>
				<view class="info-item">
					<text class="info-label">主办方</text>
					<text class="info-value">{{eventData.organizer}}</text>
				</view>
				<view class="info-item">
					<text class="info-label">报名费用</text>
					<text class="info-value">{{eventData.fee}}</text>
				</view>
				<view class="info-item">
					<text class="info-label">已报名</text>
					<text class="info-value">{{eventData.participants}}人</text>
				</view>
				<view class="info-item">
					<text class="info-label">截止时间</text>
					<text class="info-value">{{eventData.deadline}}</text>
				</view>
			</view>
			
			<view class="section">
				<view class="section-title">赛事介绍</view>
				<text class="section-content">{{eventData.description}}</text>
			</view>
			
			<view class="section">
				<view class="section-title">赛事规则</view>
				<text class="section-content">{{eventData.rules}}</text>
			</view>
			
			<view class="section">
				<view class="section-title">奖项设置</view>
				<view class="award-list">
					<view class="award-item" v-for="(item, index) in eventData.awards" :key="index">
						<view class="award-rank" :class="'rank-' + item.rank">{{item.rankName}}</view>
						<view class="award-info">
							<text class="award-name">{{item.name}}</text>
							<text class="award-desc">{{item.desc}}</text>
						</view>
					</view>
				</view>
			</view>
			
			<view class="section">
				<view class="section-title">参赛选手</view>
				<view class="participants-list">
					<view class="participant-item" v-for="(item, index) in eventData.participantList" :key="index">
						<image :src="item.avatar" class="participant-avatar"></image>
						<text class="participant-name">{{item.name}}</text>
					</view>
				</view>
			</view>
		</view>
		
		<view class="footer-action" v-if="eventData.status === 'upcoming'">
			<button class="action-btn primary" @click="register">立即报名</button>
		</view>
		
		<view class="footer-action" v-if="eventData.status === 'ongoing'">
			<button class="action-btn" @click="viewLive">观看直播</button>
			<button class="action-btn primary" @click="checkIn">现场签到</button>
		</view>
		
		<view class="footer-action" v-if="eventData.status === 'past'">
			<button class="action-btn" @click="viewHighlights">精彩回顾</button>
			<button class="action-btn primary" @click="viewResults">查看成绩</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id: 0,
				eventData: {
					id: 1,
					title: '2023年全国无人机创新应用大赛',
					status: 'upcoming',
					image: '/static/community/event1.jpg',
					time: '2023-05-20 ~ 2023-05-22',
					location: '深圳市南山区科技园创新大厦B座',
					organizer: '中国无人机产业联盟',
					fee: '个人赛: ¥200/人  团队赛: ¥500/队',
					participants: 356,
					deadline: '2023-05-15 23:59',
					description: '2023年全国无人机创新应用大赛是由中国无人机产业联盟主办的全国性赛事，旨在推动无人机技术创新与应用发展，挖掘无人机行业优秀人才。比赛分为个人技能赛和团队创新赛两个类别。',
					rules: '1. 参赛资格：\n· 个人赛：年满16周岁的无人机爱好者\n· 团队赛：2-5人组队，至少有1名成员年满18周岁',
					awards: [
						{
							rank: 1,
							rankName: '一等奖',
							name: '奖金5万元',
							desc: '获得无人机行业领先企业实习机会'
						},
						{
							rank: 2,
							rankName: '二等奖',
							name: '奖金2万元',
							desc: '获得专业无人机设备一套'
						}
					],
					participantList: [
						{ name: '航拍达人', avatar: '/static/community/avatar1.jpg' },
						{ name: '无人机教练', avatar: '/static/community/avatar2.jpg' }
					]
				}
			}
		},
		onLoad(options) {
			if (options.id) {
				this.id = options.id;
				// 这里应该根据id从服务器获取赛事详情
				// 这里使用模拟数据
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			getStatusText(status) {
				const statusTexts = {
					'upcoming': '即将开始',
					'ongoing': '进行中',
					'past': '已结束'
				};
				return statusTexts[status] || '';
			},
			register() {
				uni.navigateTo({
					url: '/pages/community/eventRegister?id=' + this.eventData.id
				});
			},
			viewLive() {
				uni.showToast({
					title: '直播功能开发中',
					icon: 'none'
				});
			},
			checkIn() {
				uni.showToast({
					title: '签到功能开发中',
					icon: 'none'
				});
			},
			viewHighlights() {
				uni.showToast({
					title: '精彩回顾功能开发中',
					icon: 'none'
				});
			},
			viewResults() {
				uni.showToast({
					title: '成绩查询功能开发中',
					icon: 'none'
				});
			}
		}
	}
</script>

<style>
	.event-detail-container {
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
	
	.share-btn {
		position: absolute;
		right: 30rpx;
	}
	
	.content-area {
		padding-bottom: 120rpx;
	}
	
	.event-banner {
		width: 100%;
		height: auto;
	}
	
	.event-header {
		padding: 30rpx;
		background-color: #fff;
		position: relative;
	}
	
	.event-title {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		padding-right: 160rpx;
	}
	
	.event-status {
		position: absolute;
		top: 30rpx;
		right: 30rpx;
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
	
	.event-info-card {
		margin: 20rpx;
		background-color: #fff;
		border-radius: 12rpx;
		padding: 20rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	
	.info-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.info-item:last-child {
		border-bottom: none;
	}
	
	.info-label {
		font-size: 28rpx;
		color: #666;
	}
	
	.info-value {
		font-size: 28rpx;
		color: #333;
		font-weight: 500;
	}
	
	.section {
		margin: 20rpx;
		background-color: #fff;
		border-radius: 12rpx;
		padding: 30rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
		position: relative;
		padding-left: 20rpx;
	}
	
	.section-title::before {
		content: '';
		position: absolute;
		left: 0;
		top: 8rpx;
		width: 8rpx;
		height: 32rpx;
		background-color: #007AFF;
		border-radius: 4rpx;
	}
	
	.section-content {
		font-size: 28rpx;
		color: #666;
		line-height: 1.6;
	}
	
	.award-list {
		margin-top: 20rpx;
	}
	
	.award-item {
		display: flex;
		align-items: center;
		margin-bottom: 20rpx;
		padding-bottom: 20rpx;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.award-item:last-child {
		margin-bottom: 0;
		padding-bottom: 0;
		border-bottom: none;
	}
	
	.award-rank {
		width: 80rpx;
		height: 80rpx;
		border-radius: 40rpx;
		background-color: #f0f0f0;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 28rpx;
		font-weight: bold;
		color: #fff;
		margin-right: 20rpx;
	}
	
	.rank-1 {
		background-color: #f5a623;
	}
	
	.rank-2 {
		background-color: #b8b8b8;
	}
	
	.participants-list {
		display: flex;
		flex-wrap: wrap;
		margin-top: 20rpx;
	}
	
	.participant-item {
		width: 120rpx;
		margin-right: 20rpx;
		margin-bottom: 20rpx;
		text-align: center;
	}
	
	.participant-avatar {
		width: 120rpx;
		height: 120rpx;
		border-radius: 60rpx;
		margin-bottom: 10rpx;
	}
	
	.participant-name {
		font-size: 24rpx;
		color: #666;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	
	.footer-action {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		display: flex;
		padding: 20rpx 30rpx;
		background-color: #fff;
		border-top: 1rpx solid #f0f0f0;
	}
	
	.action-btn {
		flex: 1;
		height: 80rpx;
		line-height: 80rpx;
		font-size: 30rpx;
		border-radius: 40rpx;
		margin: 0 10rpx;
	}
	
	.action-btn.primary {
		background-color: #007AFF;
		color: #fff;
	}
</style> 