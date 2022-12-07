import sublime
import sublime_plugin

class HbCompletions(sublime_plugin.EventListener):

	def on_query_completions(self, view, prefix, locations):
		
		if not view.match_selector(0, "text.html"):
			return None

		print_op = [
			["hb.print.echo qh($P['var_string'])\tPrint with escaping, error on undefined node access", "{=var_string}"], 
			["hb.print.echo qh(@$P['var_string'])\tPrint with escaping, NO error on undefined node access", "{=?var_string}"],
			["hb.print.echo @$P['var_string']\tPrint WITHOUT escaping, NO error on undefined node access", "{=@?var_string}"],
			["hb.print.echo $P['var_string']\tPrint WITHOUT escaping, error on undefined node access", "{=@var_string}"]
		]

		foreach_op = [
			["hb.cycles.foreach ($P['var_hash']) { }", "{#var_hash}{/#}"],
			["hb.cycles.foreach ($P['var_hash'] as $key => $value) { echo $key; echo $value; }", "{#var_hash as $key => $value}{=key}{=value}{/#}"],
			["hb.cycles.foreach ($P['var_hash'] as $key => $value) { echo $key; echo $value; }\tShortened version.\n 'foreach' construction always provides access to the current element key and value using \n 'special' nodes # and . respectively", "{#var_hash}{=#}{=.}{/#}"]
		]

		if_op = [
			["hb.construction.if ($P['var_int']){ }", "{?var_int}{/?}"],
			["hb.construction.if (@$P['var_int']){ }", "{??var_int}{/?}"],
			["hb.construction.if ($res = @$P['var_int']) { echo $res }", "{??var_int as $res}{=res}{/?}"],
			["hb.construction.if ($res = @$P['var_int']) { echo $res }\tShortened version. 'IF' construction always provides access to the first condition value using 'special' node ?", "{??var_int as $res}{=?}{/?}"],
			["hb.construction.if ($res = (@$P['var_int'] > 3)) { echo $res }", "{??var_int > 3 as $res}{=res}{/?}"],
			["hb.construction.if ($P['var_int']) {echo 'YES'} else {echo 'NO'}", "{?var_int}YES{?^}NO{/?}"],
			["hb.construction.if ($P['var_int']) {echo 'YES'} elseif ($P['var_string']) {echo 'INSTEAD'} else { echo 'NO' }", "{?var_int}YES{?^ var_string}INSTEAD{?^}NO{/?}"],
			["hb.construction.if (!$P['var_int']) { }", "{!var_int}{/!}"],
			["hb.construction.if (!@$P['var_int']) { }","{!!var_int}{/!}"]
		]

		block_op = [
			["hb.block.echo Other_View::someBlock()\tReference to block from other template file automatically includes referrenced file ( similar to PHP's autoload )", "{=/Other/View:someBlock}"],
			["hb.block.static function Template_Class::someBlock() { … }\tBlock definition. For more information see chapter 'Blocks'", "{block someBlock} … {/block}"]
		]

		block_strings = [
			["hb.string.cs", "{=NODE\tAplly sprintf 'format' to node value. If NODE is empty return "" | cs('format', 'default_value')}"],
			["hb.string.replace\tReplace all 'str_from' with 'str_to'", "{=NODE | replace('str_from', 'str_to')}"],
			["hb.string.explode\tReturns array of NODE string parts divided by 'delimeter'", "{=NODE | explode('delimeter')}"],
			["hb.string.preg_replace\tReplace all substrings mathes 'pattern' with 'str_to'", "{=NODE | preg_replace('pattern', 'str_to')}"],
			["hb.string.fm\tReturns first substring matches 'pattern'", "{=NODE | fm('pattern')}"],
			["hb.string.title\tMake all first letters uppercased, other letters - lowecased", "{=NODE | title}"],
			["hb.string.capitalize\tMake first letter uppercased, other letters - lowecased", "{=NODE | capitalize}"],
			["hb.string.upper\tMake all letters uppercased", "{=NODE | upper}"],
			["hb.string.lower\tMake all letters lowercased", "{=NODE | upper}"],
			["hb.string.concat\tConcat NODE value with other filter parameters", "{=NODE | concat('value'[, 'value2'])}"],
			["hb.string.cut\tCut string to up to 'length'", "{=NODE | cut(length)}"],
			["hb.string.h\tHTML escape NODE or all items in NODE", "{=NODE | h}"],
			["hb.string.spintf\tAplly sprintf 'format' to node value", "{=NODE | spintf('format')}"],
			["hb.string.startsWith\tIf NODE starts with 'substr', returns NODE/true value otherwize returns null", "{=NODE | startsWith('substr')}"],
			["hb.string.notStartsWith\tIf NODE DOES NOT\nstarts with 'substr', returns NODE/true value otherwize returns null", "{=NODE | notStartsWith('substr')}"],
		]

		block_arrays = [
			["hb.array.j", "{=NODE | j}"],
			["hb.array.j_escape\tJoin NODE values", "{=NODE | j('<br/>')}"],
			["hb.array.j_sprintf\tJoin NODE values. Apply sprintf format \n'sprintf_format' to each item", "{=NODE | j('<br/>', 'sprintf_format')}"],
			["hb.array.j_sprintf_escape\tJoin NODE values. Apply sprintf format\n 'sprintf_format' to each item and escape result", "{=NODE | j('<br/>', 'sprintf_format'), 1}"],
			["hb.array.jh", "{=NODE | j}"],
			["hb.array.jh_escape\tJoin NODE values. Escape results", "{=NODE | j('<br/>')}"],
			["hb.array.jh_sprintf_escape\tJoin NODE values. Apply sprintf format 'sprintf_format' to each item and escape result", "{=NODE | j('<br/>'', 'sprintf_format')}"],
			["hb.array.join", "{=NODE | join}"],
			["hb.array.join_escape\tJoin NODE values", "{=NODE | join('<br/>'')}"],

			["hb.array.first\tReturns first element of NODE array", "{=NODE | first}"],
			["hb.array.firstKey\tReturns KEY of the first element of NODE array","{=NODE | firstKey}"],
			["hb.array.last\tReturns last element of NODE array", "{=NODE | last}"],
			["hb.array.lastKey\tReturns KEY of the last element of NODE array", "{=NODE | lastKey}"],
			["hb.array.keys\tReturns array of NODE keys", "{=NODE | keys}"],
			
			["hb.array.slice_offset\tSubset of NODE array starting with 'offset' to the end", "{=NODE | slice(offset)}"],
			["hb.array.slice_offset_len\tSubset of NODE array starting with 'offset' to 'offset+length'", "{=NODE | slice(offset, length)}"],
			["hb.array.slice_offset_len_pk\tBy default 'preserve_keys' is true", "{=NODE | slice(offset, length, preserve_keys)}"],

			["hb.array.chunk\tRegroup NODE array into array of chunks 'size' elements each", "{=NODE | chunk(size)}"],
			["hb.array.reverse\tReverse NODE array", "{=NODE | reverse}"],
			["hb.array.shuffle\tShuffle NODE array", "{=NODE | shuffle}"],
			
			["hb.array.sort\tSort NODE array", "{=NODE | sort}"],
			["hb.array.sort_by_key\tSort NODE array by 'key1'", "{=NODE | sort('key1')}"],
			["hb.array.sort_by_keys\tSort NODE array by 'key1' and 'key2'", "{=NODE | sort('key1', 'key2')}"],
			
			["hb.array.rsort\tReverse sort NODE array", "{=NODE | rsort}"],
			["hb.array.rsort_by_key\tReverse sort NODE array by 'key1'", "{=NODE | rsort('key1')}"],
			["hb.array.rsort_by_keys\tReverse sort NODE array by 'key1' and 'key2'", "{=NODE | rsort('key1', 'key2')}"],

			["hb.array.ksort\tSort NODE by keys", "{=NODE | ksort}"],
			["hb.array.krsort\tReverse sort NODE by keys", "{=NODE | krsort}"],
			["hb.array.unique\tReturns only unique items from NODE arrays.","{=NODE | unique}"],
			["hb.array.remove_keys\tRemoves specified keys from NODE array", "{=NODE | remove_keys([1,3,4])}"],
			["hb.array.extract_keys\tExtract specified NON-EMPTY keys keys from NODE array", "{=NODE | extract_keys([1,3,4])}"],
			["hb.array.extract\tExtract specified key from NODE array", "{=NODE | extract('key')}"],
			["hb.array.js\tJson encoded NODE value with UNICODE + non escaped slashes + Pretty Print", "{=NODE | js}"],
			["hb.array.json\tJson encoded NODE value with UNICODE + non escaped slashes", "{=NODE | json}"],
			["hb.array.multiple\tReturns true if NODE is array\n and has more than 1 element\nExample: {=profiles | count} profile{??profiles | multiple}s{/?} found.", "{=NODE | multiple}"],
		]

		block_dt = [
			["hb.date_time.dt", "{=\\time() | dt()}"],
			["hb.date_time.dt_format\tFormat unix timestamp value to string date/time.\n Default format is 'm/d/Y h:ia'", "{=\\time() | dt('Y-m-d H:i:s')}"],
			["hb.date_time.hbdt", "{=20171102 | hbdt()}"],
			["hb.date_time.hbdt_format\tFormat HB date value (int YYYYMMDD) to string date/time.\n Default format is 'Nov 02, 2017'", "{=20171102 | hbdt(['format' => 'Y-m-d'])}"],
			["hb.date_time.date", "{=\\time() | date()}"],
			["hb.date_time.date_format\tFormat unix timestamp value to string date/time.\n Default format is 'M d, Y'", "{=\\time() | date('Y-m-d')}"],		
		]

		block_num = [
			["hb.numeric.odd\tIf NODE is odd returns NODE value, otherwise null", "{=NODE | odd}"],
			["hb.numeric.even\tIf NODE is even returns NODE value, otherwise null", "{=NODE | even}"],
			["hb.numeric.ne\tIf NODE is not empty returns NODE value, otherwise null", "{=NODE | ne}"],
			["hb.numeric.nth\tIf NODE % base === reminder returns NODE value, otherwise null", "{=NODE | nth(base,reminder)}"],
			["hb.numeric.inc\tIncrement NODE by 1 and return value", "{=NODE | inc()}"],
			["hb.numeric.inc\tIncrement NODE by 3 and return value", "{=NODE | inc(3)}"],
			["hb.numeric.dec\tDecrement NODE by 1 and return value", "{=NODE | dec()}"],
			["hb.numeric.dec\tDecrement NODE by 3 and return value", "{=NODE | dec(3)}"],					
		]

		block_cur = [
			["hb.currency.usd\tFormat value as USD. eg: $123,456.45", "{=NODE | usd()}"],
			["hb.currency.usd_format\tFormat value as USD with only decimals digits after '.'. 0 means: $123,456", "{=NODE | usd(decimals)}"],
			["hb.currency.usd_format_big\tWith 'megabucks'=true passed amount will be $123M or $20.5K. Usefull for big amounts", "{=NODE | usd(decimals, megabucks)}"],
			["hb.currency.usdc\tFormat value as USD where value is represented in CENTS. eg: $123,456.45", "{=NODE | usdc()}"],
			["hb.currency.usdc_dp\\$10.1", "{=10056| usd(1)}"],
		]

		block_geo = [
			["hb.geo.latitude\tProper formatting latitude in Rad","{=NODE | latitude}"],
			["hb.geo.latitude_grad\tProper formatting latitude in Grad\nExample: {=71.23446667 | latitude('grad')}", "{=NODE | latitude('grad')}"],
			["hb.geo.longitude\tProper formatting longitude in Rad", "{=NODE | longitude}"],
			["hb.geo.longitude_grad\tProper formatting longitude in Grad\nExample: {=71.23446667 | longitude('grad')}", "{=NODE | longitude('grad')}"],
		]


		block_other = [
			["hb.phone\tProper formatting phone number", "{=NODE | phone}"],
			["hb.phone_format\tProper formatting phone number.\n 'format_string' will be used istead of default \n\\RDSite::sitePhoneFormat() value Example: {=phone | phone('<%s>-%s.%s')}'", "{=NODE | phone('format_string')}"],
			["hb.address\tProper formatting US POST ADDRESS from NODE that has value of SH:Loc type", "{=NODE | address}"],
			["hb.not_empty\tThrow exception and stop execution if NODE is empty", "{=NODE | not_empty}"],
			["hb.filter\tDummy filter. Do nothing.", "{=NODE | filter}"]
		]

		block_debug = [
			["hb.debug.v\tDumps NODE value", "{=NODE | v}"],
			["hb.debug.vvv\tDumps NODE value in rich format.", "{=NODE | vvv}"],
		]

		block_tags = [
			["hb.tags.extends", "{%extends ClassName}"],
			["hb.tags.debug.v", "{%v G}"],
			["hb.tags.debug.v_if", "{%v G C}"],
			
			["hb.tags.debug.vvv", "{%vvv G}"],
			["hb.tags.debug.vvv_if", "{%vvv G C}"],
			
			["hb.tags.err", "{%err 'Somethin is wrong'}"],
			["hb.tags.rerr_empty\tDispaly error message and stop execution (die)", "{%err }"],
			
			["hb.tags.admin.admin\tContent inside this tag displays only to administrators", "{%admin}Some internal information{/%admin}"],
			["hb.tags.admin.xadmin\tContent inside this tag displays only to visitors\nfrom IP addresses", "{%xadmin}Some internal information{/%xadmin}"],
			
			["hb.tags.admin.adminDiv_variant1\tContent inside this tag displays only to visitors admins,\nwrapped in hidden <div> and controlled by [ + ].\nOptioanlly title could be specified.", "{%adminDiv}Some big internal information{/%adminDiv}"],
			["hb.tags.admin.adminDiv_variant2\tContent inside this tag displays only to visitors admins,\nwrapped in hidden <div> and controlled by [ + ].\nOptioanlly title could be specified.", "{%adminDiv 'Golbals:'}{=G | vvv}{/%adminDiv}"],
			["hb.tags.admin.adminDiv_variant3\tContent inside this tag displays only to visitors admins,\nwrapped in hidden <div> and controlled by [ + ].\nOptioanlly title could be specified.", "{%adminDiv G.layout}{=P | vvv}{/%adminDiv}"],


			["hb.tags.strict\tEnable/Disable strict mode. Default is 1.\nUse with caution - this is global setting", "{%strict 1}"],
			["hb.tags.show\tRenders old technology template.", "{%show '/inc/name'}"],
			
			["hb.tags.admin.info_variant1\tPlace info record to profiler.", "{%info 'Reading profiles'}"],
			["hb.tags.admin.info_variant2\tPlace info record to profiler.", "{%info 'layout' G.layout}"],
			
			["hb.tags.each_variant1\tCall block for each element of NODE array", "{%each NODE 'block'}"],
			["hb.tags.each_variant2\tCall block for each element of NODE array", "{%each profiles '/Profile/List:oneRecord'}"],


			["hb.tags.each_a_variant1\tCall block for each element of NODE array.\nCurrent node value is being passed as [a:SINGLE_VALUE].\nUseful for array of scalars iterators\nExample: {#each_a ['a', 'b'] :block}", "{%each_a NODE 'block'}"],
			["hb.tags.each_a_variant2\tCall block for each element of NODE array.\nCurrent node value is being passed as [a:SINGLE_VALUE].\nUseful for array of scalars iterators\nExample: {#each_a ['a', 'b'] :block}", "{%each_a profiles '/Profile/List:oneRecord'}"],

			["hb.tags.repeat_variant1", "{%repeat times}{$.}{/%repeat}"],
			["hb.tags.repeat_variant2", "{%repeat start times}{$.}{/%repeat}"],

			["hb.tags.range\tRepeat code for counter running from 'start' to 'end'", "{%range start end}{$.}{/%range}"],
			["hb.tags.range_step\tRepeat code for counter running from 'start' to 'end' with optional 'step'", "{%range start end step}{$.}{/%range}"],
			
			["hb.tags.odd\tDisplay code only if NODE value is odd", "{%odd NODE} ... {/%odd}"],
			
			["hb.tags.even\tDisplay code only if NODE value is even", "{%even NODE} ... {/%oeven}"],
			["hb.tags.re\tDisplay code only if NODE matches regular expression 'EXPR'", "{%re NODE EXPR} ... {/%re}"],
			
			["hb.tags.if_break\tConditional 'break' inside 'foreach' loop\nExample: {#profiles as $profile}{%if_break profile.id > 1000}{=profile.name}{/#}", "{%if_break LOGICAL_EXPRESSION}"],
			
			["hb.tags.if_continue\tConditional 'continue' inside 'foreach' loop\nExample: {#profiles as $profile}{%if_continue profile.id > 1000}{=profile.name}{/#}", "{%if_continue LOGICAL_EXPRESSION}"],
			
			["hb.tags.if_return\t'Earlier return'.\tConditional fall back from 'IF' statement.\tMultiple level of nested 'IF' breaking supported by 'level_up' parameter.", "{%if_return LOGICAL_EXPRESSION} {%if_return NODE level_up}"],
			["hb.tags.if_mod\tDisplay code only if division reminder matches eg: NODE % DIVIDER == REMINDER\nExample: {#[0 1 2 3 4 5] as $a}{%if_mod a 4 0}\nFirst column{/%if_mod}{%if_mod a 4 1}2nd column{/%if_mod}{/#}", "{%if_mod NODE DIVIDER REMINDER} ... {/%if_mod}"],
			
			["hb.tags.switch\tPHP 'Switch' analog", "{%switch node}\n{%case 'a'}...{%break}\n{%case 'b'}...{%break}\n{%case_default}...{%break}\n{/%switch}"],
			["hb.tags.if_block", "{%if_block ':BlockRaw'}BlockRaw exists{/%if_block}"],
			["hb.tags.if_block_else", "{%if_block ':BlockRawXX'}BlockRawXX exists{%else}BlockRawXX does not exist{/%if_block}"],

			["hb.tags.formatting.trim\tTrim all lines in tag content", "{%trim}...{/%trim}"],

			["hb.tags.formatting.j\tDisplay join() of NODE array with optional\n 'delimeter' and optioanl sprintf() formatted of each element", "{%j NODE}"],
			["hb.tags.formatting.j_delimeter\tDisplay join() of NODE array with optional\n 'delimeter' and optioanl sprintf() formatted of each element", "{%j NODE delimeter}"],
			["hb.tags.formatting.j_delimeter_foramt\tDisplay join() of NODE array with optional\n 'delimeter' and optioanl sprintf() formatted of each element", "{%j NODE delimeter format_string}"],

			["hb.tags.formatting.jh", "{%jh NODE}"],
			["hb.tags.formatting.jh_delimeter", "{%jh NODE delimeter}"],
			["hb.tags.formatting.jh_delimeter_foramt", "{%jh NODE delimeter format_string}"],

			["hb.tags.set_unset.set\tAssign VALUE to NODE", "{%set NODE VALUE}"],
			["hb.tags.set_unset.set_tag\tAssign tag content to NODE", "{%set}some code{/%set NODE}"],

			["hb.tags.set_unset.unset\tUnnset NODE", "{%unset NODE}"],
			["hb.tags.set_unset.unecho\tEcho NODE then unset NODE", "{%unecho NODE}"],
			["hb.tags.set_unset.uset\tMove NODE-SOURCE to NODE-DEST. Some sort of rename.", "{%uset NODE-DEST NODE-SOURCE}"],

			["hb.tags.set_unset.push\tAppend VALUE to NODE array", "{%push NODE VALUE}"],
			["hb.tags.set_unset.push_tag\tAppend tag content to NODE array", "{%push}some code{/%push NODE}"],
			
			["hb.tags.set_unset.pushNE\tAppend VALUE to NODE array if VALUE is not empty", "{%pushNE NODE VALUE}"],
			["hb.tags.set_unset.pushNE_tag\tAppend tag content to NODE array if content is not empty", "{%pushNE}some code{/%pushNE NODE}"],

			["hb.tags.set_unset.unshift\tPrepend VALUE to NODE array", "{%unshift NODE VALUE}"],
			["hb.tags.set_unset.unshift_tag\tPrepend tag content to NODE array", "{%unshift}some code{/%unshift NODE}"],

			["hb.tags.set_unset.pop\tRemove last element from NODE and print it escaped", "{%pop NODE}"],

			["hb.tags.set_unset.shift\tRemove first element from NODE and print it escaped", "{%shift NODE}"],
			
			["hb.tags.set_unset.first\tPrint first element from NODE escaped", "{%first NODE}"],
			
			["hb.tags.set_unset.last\tPrint last element from NODE escaped", "{%last NODE}"],

			["hb.tags.set_unset.inc\tIncrement NODE value by 'BY'", "{%inc NODE BY}"],

			["hb.tags.set_unset.dec\tDecrement NODE value by 'BY'", "{%dec NODE BY}"],

			["hb.tags.urls.url\tBuilds URL", "{%url 'url' params}"],
			["hb.tags.urls.url_get\tOnly 'GET' part", "{%url '' params}"],
			["hb.tags.urls.url_this\tURI of this page", "{%url true params}"],
			["hb.tags.urls.url_other\tURI of other page", "{%url '/some/page' params}"],
			["hb.tags.urls.url_by_alias\tURL by alias", "{%url '@alias' params}"],
			["hb.tags.urls.href", "{%href 'url' params}"],
			["hb.tags.urls.src", "{%src 'url' params}"],
			["hb.tags.urls.action", "{%action 'url' params}"],
			
		]

		out = (print_op +
			foreach_op + 
			if_op + 
			block_op + 
			block_strings + 
			block_arrays + 
			block_dt +
			block_num +
			block_cur +
			block_geo +
			block_other +
			block_debug +
			block_tags
			)

		return out

