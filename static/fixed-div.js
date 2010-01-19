window.onscroll = function()
{
	var item=document.getElementById('fixed-div');
	var parentBlock=document.getElementById('main');
	var topHeight=parentBlock.offsetTop;
	if ( parentBlock.offsetTop+parentBlock.offsetHeight-document.documentElement.scrollTop-item.offsetHeight-100 <0 || parentBlock.offsetTop+parentBlock.offsetHeight-self.pageYOffset-item.offsetHeight-100 <0 ){
			item.style.position = 'absolute';
			item.style.top = (parentBlock.offsetTop+parentBlock.offsetHeight-item.offsetHeight-100 )+'px';
	}	else if ( document.documentElement.scrollTop > topHeight || self.pageYOffset > topHeight ) {
			item.style.position = 'fixed';
			item.style.top = '0';
	} else if (document.documentElement.scrollTop < topHeight || self.pageYOffset < topHeight) {
			item.style.position = 'absolute';
			item.style.top = topHeight+'px';
	}
}