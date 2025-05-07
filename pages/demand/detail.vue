<template>
	<view class="detail-container">
		<!-- 需求信息部分 -->
		<view class="detail-section demand-info">
			<view class="demand-header">
				<text class="demand-title">{{demandData.title}}</text>
				<view class="demand-meta">
					<text class="demand-type">{{demandData.type}}</text>
					<text class="demand-status" :class="{'status-urgent': demandData.isUrgent}">
						{{demandData.isUrgent ? '紧急' : '普通'}}
					</text>
				</view>
			</view>
			
			<view class="demand-budget">
				<text class="budget-label">预算：</text>
				<text class="budget-value">¥{{demandData.budget}}</text>
			</view>
			
			<view class="demand-row">
				<text class="row-label">发布人：</text>
				<text class="row-value">{{demandData.publisher}}</text>
			</view>
			
			<view class="demand-row">
				<text class="row-label">联系方式：</text>
				<text class="row-value contact-value" @tap="makePhoneCall">{{demandData.contact}}</text>
			</view>
			
			<view class="demand-row">
				<text class="row-label">服务区域：</text>
				<text class="row-value">{{demandData.region}}</text>
			</view>
			
			<view class="demand-row">
				<text class="row-label">发布时间：</text>
				<text class="row-value">{{demandData.publishTime}}</text>
			</view>
			
			<view class="demand-row">
				<text class="row-label">截止日期：</text>
				<text class="row-value">{{demandData.deadline}}</text>
			</view>
		</view>
		
		<!-- 需求详情描述 -->
		<view class="detail-section demand-description">
			<view class="section-title">需求详情</view>
			<text class="description-content">{{demandData.description}}</text>
		</view>
		
		<!-- 图片展示区域 -->
		<view class="detail-section demand-images" v-if="demandData.images && demandData.images.length > 0">
			<view class="section-title">相关图片</view>
			<view class="image-list">
				<image 
					class="demand-image" 
					v-for="(img, index) in demandData.images" 
					:key="index" 
					:src="img" 
					mode="aspectFill"
					@tap="previewImage(index)"
				></image>
			</view>
		</view>
		
		<!-- 报价按钮 -->
		<view class="action-bar">
			<button class="action-button collect-button" @tap="toggleCollect">
				<text class="button-icon" :class="{'icon-collected': isCollected}">★</text>
				<text>{{isCollected ? '已收藏' : '收藏'}}</text>
			</button>
			<button class="action-button contact-button" @tap="contactPublisher">联系发布者</button>
			<button class="action-button quote-button" @tap="showQuoteForm">我要报价</button>
		</view>
		
		<!-- 报价表单弹窗 -->
		<view class="quote-popup" v-if="showQuote">
			<view class="quote-form">
				<view class="form-header">
					<text class="form-title">报价</text>
					<text class="close-icon" @tap="hideQuoteForm">×</text>
				</view>
				
				<view class="form-item">
					<text class="form-label">报价金额</text>
					<input class="form-input" v-model="quoteForm.price" type="digit" placeholder="请输入您的报价金额" />
				</view>
				
				<view class="form-item">
					<text class="form-label">完成周期</text>
					<input class="form-input" v-model="quoteForm.duration" type="number" placeholder="请输入预计完成天数" />
				</view>
				
				<view class="form-item">
					<text class="form-label">服务说明</text>
					<textarea class="form-textarea" v-model="quoteForm.description" placeholder="请详细描述您的服务内容和优势" />
				</view>
				
				<button class="submit-button" @tap="submitQuote">提交报价</button>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				demandId: null,
				demandData: {
					id: 1,
					title: '农田植保作业服务需求',
					type: '植保服务',
					isUrgent: true,
					budget: '2000',
					publisher: '李农夫',
					contact: '13812345678',
					region: '河南省 周口市 商水县',
					publishTime: '2023-04-10',
					deadline: '2023-04-25',
					description: '需要对100亩小麦农田进行农药喷洒作业，农田位于河南周口商水县谭庄镇，地形平坦，农作物为小麦，目前处于抽穗期，需要防治病虫害。要求使用专业植保无人机，药剂自备，需要在三天内完成作业。\n\n服务要求：\n1. 需持有无人机植保作业资质\n2. 需提供作业后的电子作业记录和报告\n3. 保证作业均匀度和覆盖率\n4. 如遇天气原因无法作业，可协商延期',
					images: [
						'../../static/images/tabbar/home.jpg',
						'../../static/images/tabbar/demand.jpg',
						'../../static/images/tabbar/service.png'
					]
				},
				isCollected: false,
				showQuote: false,
				quoteForm: {
					price: '',
					duration: '',
					description: ''
				}
			}
		},
		onLoad(options) {
			// 获取传递的需求ID
			if (options.id) {
				this.demandId = options.id;
				this.loadDemandDetail();
			}
		},
		methods: {
			loadDemandDetail() {
				// 实际开发中，这里应该是API请求获取需求详情
				// 这里使用的是模拟数据，可以根据ID做一些变化
				if (this.demandId == 2) {
					this.demandData.title = '城市建筑航拍服务需求';
					this.demandData.type = '航拍服务';
					this.demandData.isUrgent = false;
					this.demandData.budget = '5000';
					this.demandData.publisher = '张导演';
					this.demandData.region = '广东省 广州市 天河区';
					this.demandData.description = '需要专业航拍团队拍摄城市建筑宣传片，时长5分钟，以广州天河CBD核心区域为主，需要包含日出、日落、夜景等不同时段的画面，要求4K分辨率。\n\n要求：\n1. 有相关企业宣传片拍摄经验\n2. 提供样片参考\n3. 有专业航拍资质和设备\n4. 可以根据需求调整拍摄方案';
				} else if (this.demandId == 3) {
					this.demandData.title = '电力线路巡检服务需求';
					this.demandData.type = '巡检服务';
					this.demandData.isUrgent = true;
					this.demandData.budget = '3000';
					this.demandData.publisher = '国网运维';
					this.demandData.region = '浙江省 杭州市 萧山区';
					this.demandData.description = '需要对50公里电力线路进行日常巡检，地点位于杭州萧山区，需要使用热成像设备进行隐患排查，要求生成巡检报告并标注问题点位置。\n\n要求：\n1. 有电力巡检资质和经验\n2. 配备热成像和高清摄像设备\n3. 能提供规范化巡检报告\n4. 一周内完成巡检任务';
				}
			},
			makePhoneCall() {
				uni.makePhoneCall({
					phoneNumber: this.demandData.contact
				});
			},
			previewImage(index) {
				uni.previewImage({
					current: this.demandData.images[index],
					urls: this.demandData.images
				});
			},
			toggleCollect() {
				this.isCollected = !this.isCollected;
				uni.showToast({
					title: this.isCollected ? '收藏成功' : '已取消收藏',
					icon: 'success'
				});
			},
			contactPublisher() {
				uni.navigateTo({
					url: '/pages/community/chat?userId=' + this.demandData.publisher
				});
			},
			showQuoteForm() {
				this.showQuote = true;
			},
			hideQuoteForm() {
				this.showQuote = false;
			},
			submitQuote() {
				// 验证表单
				if (!this.quoteForm.price) {
					uni.showToast({
						title: '请输入报价金额',
						icon: 'none'
					});
					return;
				}
				
				if (!this.quoteForm.duration) {
					uni.showToast({
						title: '请输入完成周期',
						icon: 'none'
					});
					return;
				}
				
				if (!this.quoteForm.description) {
					uni.showToast({
						title: '请输入服务说明',
						icon: 'none'
					});
					return;
				}
				
				// 显示提交中
				uni.showLoading({
					title: '提交中...'
				});
				
				// 模拟提交
				setTimeout(() => {
					uni.hideLoading();
					
					uni.showToast({
						title: '报价提交成功',
						icon: 'success'
					});
					
					// 隐藏表单
					this.hideQuoteForm();
					
					// 清空表单
					this.quoteForm = {
						price: '',
						duration: '',
						description: ''
					};
				}, 1500);
			}
		}
	}
</script>

<style>
	.detail-container {
		padding-bottom: 120rpx;
		background-color: #f5f5f5;
	}
	
	.detail-section {
		background-color: #fff;
		margin-bottom: 20rpx;
		padding: 30rpx;
	}
	
	.demand-header {
		border-bottom: 1rpx solid #eee;
		padding-bottom: 20rpx;
		margin-bottom: 20rpx;
	}
	
	.demand-title {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 16rpx;
		display: block;
	}
	
	.demand-meta {
		display: flex;
		align-items: center;
	}
	
	.demand-type, .demand-status {
		padding: 4rpx 12rpx;
		border-radius: 4rpx;
		font-size: 24rpx;
		margin-right: 16rpx;
	}
	
	.demand-type {
		background-color: #e6f7ff;
		color: #1890ff;
	}
	
	.demand-status {
		background-color: #f6ffed;
		color: #52c41a;
	}
	
	.status-urgent {
		background-color: #fff2f0;
		color: #ff4d4f;
	}
	
	.demand-budget {
		display: flex;
		align-items: center;
		margin-bottom: 20rpx;
	}
	
	.budget-label {
		font-size: 28rpx;
		color: #333;
	}
	
	.budget-value {
		font-size: 36rpx;
		color: #ff4d4f;
		font-weight: bold;
	}
	
	.demand-row {
		display: flex;
		margin-bottom: 16rpx;
	}
	
	.row-label {
		width: 140rpx;
		font-size: 28rpx;
		color: #666;
	}
	
	.row-value {
		flex: 1;
		font-size: 28rpx;
		color: #333;
	}
	
	.contact-value {
		color: #1890ff;
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
		padding-bottom: 16rpx;
		border-bottom: 1rpx solid #eee;
	}
	
	.description-content {
		font-size: 28rpx;
		color: #333;
		line-height: 1.6;
		white-space: pre-wrap;
	}
	
	.image-list {
		display: flex;
		flex-wrap: wrap;
	}
	
	.demand-image {
		width: 214rpx;
		height: 214rpx;
		margin-right: 15rpx;
		margin-bottom: 15rpx;
		border-radius: 8rpx;
	}
	
	.demand-image:nth-child(3n) {
		margin-right: 0;
	}
	
	.action-bar {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 0;
		height: 100rpx;
		background-color: #fff;
		display: flex;
		border-top: 1rpx solid #eee;
	}
	
	.action-button {
		flex: 1;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		border-radius: 0;
		font-size: 24rpx;
		color: #666;
		background-color: #fff;
		margin: 0;
		padding: 0;
		line-height: 1.5;
	}
	
	.button-icon {
		font-size: 32rpx;
		margin-bottom: 6rpx;
		color: #999;
	}
	
	.icon-collected {
		color: #ffac38;
	}
	
	.quote-button {
		flex: 1.5;
		background-color: #007AFF;
		color: #fff;
	}
	
	.quote-popup {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.6);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 999;
	}
	
	.quote-form {
		width: 90%;
		background-color: #fff;
		border-radius: 12rpx;
		overflow: hidden;
	}
	
	.form-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #eee;
	}
	
	.form-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
	
	.close-icon {
		font-size: 40rpx;
		color: #999;
	}
	
	.form-item {
		padding: 20rpx 30rpx;
	}
	
	.form-label {
		display: block;
		font-size: 28rpx;
		color: #333;
		margin-bottom: 16rpx;
	}
	
	.form-input {
		width: 100%;
		height: 80rpx;
		background-color: #f5f5f5;
		border-radius: 6rpx;
		padding: 0 20rpx;
		font-size: 28rpx;
	}
	
	.form-textarea {
		width: 100%;
		height: 200rpx;
		background-color: #f5f5f5;
		border-radius: 6rpx;
		padding: 20rpx;
		font-size: 28rpx;
	}
	
	.submit-button {
		margin: 30rpx;
		height: 80rpx;
		line-height: 80rpx;
		background-color: #007AFF;
		color: #fff;
		border-radius: 40rpx;
		font-size: 28rpx;
	}
</style> 