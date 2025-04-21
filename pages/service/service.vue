<template>
	<view class="service-container">
		<view class="search-bar">
			<view class="search-input">
				<text class="iconfont icon-search"></text>
				<input type="text" placeholder="搜索服务类型、供应商..." />
			</view>
		</view>
		
		<view class="filter-section">
			<scroll-view scroll-x class="category-scroll">
				<view class="category-list">
					<view 
						class="category-item" 
						:class="{ active: currentCategory === category.id }" 
						v-for="(category, index) in categories" 
						:key="index"
						@click="selectCategory(category.id)"
					>
						<text>{{category.name}}</text>
					</view>
				</view>
			</scroll-view>
			
			<view class="filter-options">
				<view class="filter-item" @click="showFilterPopup('region')">
					<text>地区</text>
					<text class="iconfont icon-down"></text>
				</view>
				<view class="filter-item" @click="showFilterPopup('price')">
					<text>价格</text>
					<text class="iconfont icon-down"></text>
				</view>
				<view class="filter-item" @click="showFilterPopup('sort')">
					<text>排序</text>
					<text class="iconfont icon-down"></text>
				</view>
			</view>
		</view>
		
		<view class="service-list">
			<view class="service-item" v-for="(item, index) in filteredServices" :key="index" @click="viewServiceDetail(item.id)">
				<image :src="item.image" mode="aspectFill" class="service-image"></image>
				<view class="service-info">
					<view class="service-title">{{item.title}}</view>
					<view class="service-tags">
						<view class="service-tag" v-for="(tag, tagIndex) in item.tags" :key="tagIndex">{{tag}}</view>
					</view>
					<view class="service-price">¥{{item.price}}<text class="price-unit">{{item.unit}}</text></view>
					<view class="service-footer">
						<view class="service-provider">
							<image :src="item.providerAvatar" class="provider-avatar"></image>
							<text class="provider-name">{{item.providerName}}</text>
						</view>
						<view class="service-rating">
							<text class="rating-score">{{item.rating}}分</text>
							<text class="order-count">{{item.orderCount}}单</text>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 筛选弹窗 -->
		<view class="filter-popup" v-if="showPopup">
			<view class="popup-mask" @click="hidePopup"></view>
			<view class="popup-content">
				<view class="popup-header">
					<text class="popup-title">{{popupTitle}}</text>
					<text class="popup-close" @click="hidePopup">×</text>
				</view>
				
				<view class="popup-body">
					<!-- 地区筛选 -->
					<view v-if="currentPopup === 'region'" class="filter-option-list">
						<view 
							class="filter-option-item" 
							:class="{ active: selectedRegion === region.id }" 
							v-for="(region, index) in regions" 
							:key="index"
							@click="selectRegion(region.id)"
						>
							<text>{{region.name}}</text>
						</view>
					</view>
					
					<!-- 价格筛选 -->
					<view v-if="currentPopup === 'price'" class="filter-option-list">
						<view 
							class="filter-option-item" 
							:class="{ active: selectedPrice === price.id }" 
							v-for="(price, index) in prices" 
							:key="index"
							@click="selectPrice(price.id)"
						>
							<text>{{price.name}}</text>
						</view>
					</view>
					
					<!-- 排序筛选 -->
					<view v-if="currentPopup === 'sort'" class="filter-option-list">
						<view 
							class="filter-option-item" 
							:class="{ active: selectedSort === sort.id }" 
							v-for="(sort, index) in sorts" 
							:key="index"
							@click="selectSort(sort.id)"
						>
							<text>{{sort.name}}</text>
						</view>
					</view>
				</view>
				
				<view class="popup-footer">
					<view class="popup-btn btn-reset" @click="resetFilter">重置</view>
					<view class="popup-btn btn-confirm" @click="confirmFilter">确定</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				currentCategory: 'all',
				selectedRegion: 'all',
				selectedPrice: 'all',
				selectedSort: 'default',
				showPopup: false,
				currentPopup: '',
				popupTitle: '',
				categories: [
					{id: 'all', name: '全部'},
					{id: 'aerial', name: '航拍服务'},
					{id: 'plant', name: '植保作业'},
					{id: 'inspection', name: '巡检服务'},
					{id: 'mapping', name: '测绘服务'},
					{id: 'training', name: '培训服务'}
				],
				regions: [
					{id: 'all', name: '全部地区'},
					{id: 'north', name: '华北地区'},
					{id: 'east', name: '华东地区'},
					{id: 'south', name: '华南地区'},
					{id: 'central', name: '华中地区'},
					{id: 'southwest', name: '西南地区'},
					{id: 'northwest', name: '西北地区'},
					{id: 'northeast', name: '东北地区'}
				],
				prices: [
					{id: 'all', name: '全部价格'},
					{id: 'under1000', name: '1000元以下'},
					{id: '1000to3000', name: '1000-3000元'},
					{id: '3000to5000', name: '3000-5000元'},
					{id: 'above5000', name: '5000元以上'}
				],
				sorts: [
					{id: 'default', name: '默认排序'},
					{id: 'priceAsc', name: '价格从低到高'},
					{id: 'priceDesc', name: '价格从高到低'},
					{id: 'ratingDesc', name: '评分从高到低'},
					{id: 'orderDesc', name: '订单量从高到低'}
				],
				services: [
					{
						id: 1,
						title: '专业无人机航拍服务',
						image: '/static/tabbar/home.png',
						tags: ['4K高清', '专业团队', '后期制作'],
						price: '1500',
						unit: '起/次',
						providerName: '天翼航空',
						providerAvatar: '/static/tabbar/my.png',
						rating: '4.9',
						orderCount: '258',
						category: 'aerial',
						region: 'east'
					},
					{
						id: 2,
						title: '农田植保无人机喷洒服务',
						image: '/static/tabbar/service.png',
						tags: ['高效喷洒', '精准作业', '专业团队'],
						price: '30',
						unit: '/亩',
						providerName: '绿农植保',
						providerAvatar: '/static/tabbar/demand.png',
						rating: '4.7',
						orderCount: '189',
						category: 'plant',
						region: 'central'
					},
					{
						id: 3,
						title: '电力线路无人机巡检服务',
						image: '/static/tabbar/demand.png',
						tags: ['热成像', '高清摄像', '数据分析'],
						price: '2500',
						unit: '/次',
						providerName: '航天科技',
						providerAvatar: '/static/tabbar/community.png',
						rating: '4.8',
						orderCount: '156',
						category: 'inspection',
						region: 'north'
					},
					{
						id: 4,
						title: '无人机测绘建模服务',
						image: '/static/tabbar/community.png',
						tags: ['3D建模', '高精度', '快速交付'],
						price: '5000',
						unit: '起/项目',
						providerName: '航天科技',
						providerAvatar: '/static/tabbar/home.png',
						rating: '4.9',
						orderCount: '98',
						category: 'mapping',
						region: 'east'
					},
					{
						id: 5,
						title: '无人机专业飞行培训',
						image: '/static/tabbar/my.png',
						tags: ['持证教练', '实操训练', '证书颁发'],
						price: '3800',
						unit: '/人',
						providerName: '云端航拍',
						providerAvatar: '/static/tabbar/service.png',
						rating: '4.6',
						orderCount: '76',
						category: 'training',
						region: 'south'
					}
				]
			}
		},
		computed: {
			filteredServices() {
				let result = this.services;
				
				// 按类别筛选
				if (this.currentCategory !== 'all') {
					result = result.filter(item => item.category === this.currentCategory);
				}
				
				// 按地区筛选
				if (this.selectedRegion !== 'all') {
					result = result.filter(item => item.region === this.selectedRegion);
				}
				
				// 按价格筛选 (实际开发中需要根据具体逻辑实现)
				// 按排序规则排序 (实际开发中需要根据具体逻辑实现)
				
				return result;
			}
		},
		methods: {
			selectCategory(categoryId) {
				this.currentCategory = categoryId;
			},
			showFilterPopup(type) {
				this.currentPopup = type;
				switch(type) {
					case 'region':
						this.popupTitle = '选择地区';
						break;
					case 'price':
						this.popupTitle = '价格区间';
						break;
					case 'sort':
						this.popupTitle = '排序方式';
						break;
				}
				this.showPopup = true;
			},
			hidePopup() {
				this.showPopup = false;
			},
			selectRegion(regionId) {
				this.selectedRegion = regionId;
			},
			selectPrice(priceId) {
				this.selectedPrice = priceId;
			},
			selectSort(sortId) {
				this.selectedSort = sortId;
			},
			resetFilter() {
				switch(this.currentPopup) {
					case 'region':
						this.selectedRegion = 'all';
						break;
					case 'price':
						this.selectedPrice = 'all';
						break;
					case 'sort':
						this.selectedSort = 'default';
						break;
				}
			},
			confirmFilter() {
				this.hidePopup();
				// 在实际应用中可能需要调用API重新获取数据
			},
			viewServiceDetail(id) {
				uni.navigateTo({
					url: '/pages/service/detail?id=' + id
				});
			}
		}
	}
</script>

<style>
	.service-container {
		min-height: 100vh;
		background-color: #f5f5f5;
		position: relative;
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
	
	.filter-section {
		background-color: #fff;
		padding-bottom: 10rpx;
	}
	
	.category-scroll {
		white-space: nowrap;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}
	
	.category-list {
		padding: 0 20rpx;
		display: inline-block;
	}
	
	.category-item {
		display: inline-block;
		padding: 10rpx 30rpx;
		margin-right: 20rpx;
		font-size: 28rpx;
		color: #666;
		background-color: #f5f5f5;
		border-radius: 30rpx;
	}
	
	.category-item.active {
		background-color: #007AFF;
		color: #fff;
	}
	
	.filter-options {
		display: flex;
		padding: 20rpx 30rpx;
	}
	
	.filter-item {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 26rpx;
		color: #666;
	}
	
	.icon-down {
		margin-left: 6rpx;
		font-size: 24rpx;
	}
	
	.service-list {
		padding: 20rpx;
	}
	
	.service-item {
		display: flex;
		background-color: #fff;
		border-radius: 12rpx;
		margin-bottom: 20rpx;
		overflow: hidden;
	}
	
	.service-image {
		width: 240rpx;
		height: 240rpx;
		flex-shrink: 0;
	}
	
	.service-info {
		flex: 1;
		padding: 20rpx;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
	
	.service-title {
		font-size: 30rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.service-tags {
		display: flex;
		flex-wrap: wrap;
		margin-bottom: 10rpx;
	}
	
	.service-tag {
		font-size: 22rpx;
		padding: 4rpx 10rpx;
		background-color: #f0f7ff;
		color: #007AFF;
		border-radius: 4rpx;
		margin-right: 10rpx;
		margin-bottom: 10rpx;
	}
	
	.service-price {
		font-size: 34rpx;
		color: #ff6600;
		font-weight: bold;
		margin-bottom: 10rpx;
	}
	
	.price-unit {
		font-size: 24rpx;
		color: #999;
		font-weight: normal;
		margin-left: 4rpx;
	}
	
	.service-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.service-provider {
		display: flex;
		align-items: center;
	}
	
	.provider-avatar {
		width: 40rpx;
		height: 40rpx;
		border-radius: 50%;
		margin-right: 10rpx;
	}
	
	.provider-name {
		font-size: 24rpx;
		color: #666;
	}
	
	.service-rating {
		display: flex;
		font-size: 24rpx;
		color: #999;
	}
	
	.rating-score {
		color: #ff6600;
		margin-right: 10rpx;
	}
	
	/* 筛选弹窗样式 */
	.filter-popup {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 100;
	}
	
	.popup-mask {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
	}
	
	.popup-content {
		position: absolute;
		bottom: 0;
		left: 0;
		width: 100%;
		background-color: #fff;
		border-top-left-radius: 20rpx;
		border-top-right-radius: 20rpx;
	}
	
	.popup-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #eee;
	}
	
	.popup-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
	
	.popup-close {
		font-size: 40rpx;
		color: #999;
	}
	
	.popup-body {
		max-height: 600rpx;
		overflow-y: auto;
		padding: 20rpx 30rpx;
	}
	
	.filter-option-list {
		display: flex;
		flex-wrap: wrap;
	}
	
	.filter-option-item {
		width: 30%;
		height: 70rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 1rpx solid #eee;
		border-radius: 8rpx;
		margin-right: 3%;
		margin-bottom: 20rpx;
		font-size: 26rpx;
		color: #666;
	}
	
	.filter-option-item.active {
		border-color: #007AFF;
		color: #007AFF;
		background-color: #f0f7ff;
	}
	
	.popup-footer {
		display: flex;
		padding: 20rpx 30rpx;
		border-top: 1rpx solid #eee;
	}
	
	.popup-btn {
		flex: 1;
		height: 80rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 28rpx;
		border-radius: 8rpx;
	}
	
	.btn-reset {
		color: #666;
		background-color: #f5f5f5;
		margin-right: 20rpx;
	}
	
	.btn-confirm {
		color: #fff;
		background-color: #007AFF;
	}
</style> 