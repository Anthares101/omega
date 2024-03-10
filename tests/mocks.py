wp_url = 'http://fancy-wordpress-site.com'

xmlrpc_wrong_credentials_response = """
<methodResponse>
  <fault>
    <value>
      <struct>
        <member>
          <name>faultCode</name>
          <value><int>403</int></value>
        </member>
        <member>
          <name>faultString</name>
          <value><string>Incorrect username or password.</string></value>
        </member>
      </struct>
    </value>
  </fault>
</methodResponse>
"""

xmlrpc_right_admin_credentials_response = """
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><struct>
  <member><name>isAdmin</name><value><boolean>1</boolean></value></member>
  <member><name>url</name><value><string>http://fancy-wordpress-site.com/</string></value></member>
  <member><name>blogid</name><value><string>1</string></value></member>
  <member><name>blogName</name><value><string>Omega</string></value></member>
  <member><name>xmlrpc</name><value><string>http://fancy-wordpress-site.com/xmlrpc.php</string></value></member>
</struct></value>
</data></array>
      </value>
    </param>
  </params>
</methodResponse>
"""

xmlrpc_right_not_admin_credentials_response = """
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><struct>
  <member><name>isAdmin</name><value><boolean>0</boolean></value></member>
  <member><name>url</name><value><string>http://fancy-wordpress-site.com/</string></value></member>
  <member><name>blogid</name><value><string>1</string></value></member>
  <member><name>blogName</name><value><string>Omega</string></value></member>
  <member><name>xmlrpc</name><value><string>http://fancy-wordpress-site.com/xmlrpc.php</string></value></member>
</struct></value>
</data></array>
      </value>
    </param>
  </params>
</methodResponse>
"""

wordpress_themes_response = '<div class="theme active"><h2 class="theme-name" id="twentytwentyfour-id">Fancy theme</h2></div>'

wordpress_theme_editor_response = """<form name="template" id="template" action="theme-editor.php" method="post">
		<input type="hidden" id="nonce" name="nonce" value="43378adeff" /><input type="hidden" name="_wp_http_referer" value="/wp-admin/theme-editor.php?file=patterns%2Ffooter.php&#038;theme=twentytwentyfour" />		<div>
			<label for="newcontent" id="theme-plugin-editor-label">Selected file content:</label>
			<textarea cols="70" rows="30" name="newcontent" id="newcontent" aria-describedby="editor-keyboard-trap-help-1 editor-keyboard-trap-help-2 editor-keyboard-trap-help-3 editor-keyboard-trap-help-4">&lt;?php
/**
 * Title: Footer with colophon, 4 columns
 * Slug: twentytwentyfour/footer
 * Categories: footer
 * Block Types: core/template-part/footer
 */
?&gt;

&lt;!-- wp:group {&quot;style&quot;:{&quot;spacing&quot;:{&quot;padding&quot;:{&quot;top&quot;:&quot;var:preset|spacing|50&quot;,&quot;bottom&quot;:&quot;var:preset|spacing|50&quot;}}},&quot;layout&quot;:{&quot;type&quot;:&quot;constrained&quot;}} --&gt;
&lt;div class=&quot;wp-block-group&quot; style=&quot;padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)&quot;&gt;
	&lt;!-- wp:columns {&quot;align&quot;:&quot;wide&quot;} --&gt;
	&lt;div class=&quot;wp-block-columns alignwide&quot;&gt;
		&lt;!-- wp:column {&quot;width&quot;:&quot;30%&quot;} --&gt;
		&lt;div class=&quot;wp-block-column&quot; style=&quot;flex-basis:30%&quot;&gt;
			&lt;!-- wp:group {&quot;style&quot;:{&quot;dimensions&quot;:{&quot;minHeight&quot;:&quot;&quot;},&quot;layout&quot;:{&quot;selfStretch&quot;:&quot;fit&quot;,&quot;flexSize&quot;:null}},&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;}} --&gt;
			&lt;div class=&quot;wp-block-group&quot;&gt;
				&lt;!-- wp:site-logo {&quot;width&quot;:20,&quot;shouldSyncIcon&quot;:true,&quot;style&quot;:{&quot;layout&quot;:{&quot;selfStretch&quot;:&quot;fit&quot;,&quot;flexSize&quot;:null}}} /--&gt;

				&lt;!-- wp:site-title {&quot;level&quot;:0,&quot;fontSize&quot;:&quot;medium&quot;} /--&gt;

				&lt;!-- wp:site-tagline {&quot;fontSize&quot;:&quot;small&quot;} /--&gt;
			&lt;/div&gt;
			&lt;!-- /wp:group --&gt;
		&lt;/div&gt;
		&lt;!-- /wp:column --&gt;

		&lt;!-- wp:column {&quot;width&quot;:&quot;20%&quot;} --&gt;
		&lt;div class=&quot;wp-block-column&quot; style=&quot;flex-basis:20%&quot;&gt;
		&lt;/div&gt;
		&lt;!-- /wp:column --&gt;

		&lt;!-- wp:column {&quot;width&quot;:&quot;50%&quot;} --&gt;
		&lt;div class=&quot;wp-block-column&quot; style=&quot;flex-basis:50%&quot;&gt;
			&lt;!-- wp:group {&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;flexWrap&quot;:&quot;wrap&quot;,&quot;justifyContent&quot;:&quot;space-between&quot;,&quot;verticalAlignment&quot;:&quot;top&quot;}} --&gt;
			&lt;div class=&quot;wp-block-group&quot;&gt;
				&lt;!-- wp:group {&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;,&quot;justifyContent&quot;:&quot;stretch&quot;}} --&gt;
				&lt;div class=&quot;wp-block-group&quot;&gt;
					&lt;!-- wp:heading {&quot;level&quot;:2,&quot;style&quot;:{&quot;typography&quot;:{&quot;fontStyle&quot;:&quot;normal&quot;,&quot;fontWeight&quot;:&quot;600&quot;}},&quot;fontFamily&quot;:&quot;body&quot;} --&gt;
					&lt;h2 class=&quot;wp-block-heading has-medium-font-size has-body-font-family&quot; style=&quot;font-style:normal;font-weight:600&quot;&gt;&lt;?php esc_html_e( &#039;About&#039;, &#039;twentytwentyfour&#039; ); ?&gt;&lt;/h2&gt;
					&lt;!-- /wp:heading --&gt;

					&lt;!-- wp:group {&quot;style&quot;:{&quot;spacing&quot;:{&quot;blockGap&quot;:&quot;var:preset|spacing|10&quot;}},&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;}} --&gt;
					&lt;div class=&quot;wp-block-group&quot;&gt;

						&lt;!-- wp:navigation {&quot;overlayMenu&quot;:&quot;never&quot;,&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;},&quot;style&quot;:{&quot;typography&quot;:{&quot;fontStyle&quot;:&quot;normal&quot;,&quot;fontWeight&quot;:&quot;400&quot;},&quot;spacing&quot;:{&quot;blockGap&quot;:&quot;var:preset|spacing|10&quot;}},&quot;fontSize&quot;:&quot;small&quot;,&quot;ariaLabel&quot;:&quot;&lt;?php esc_attr_e( &#039;About&#039;, &#039;twentytwentyfour&#039; ); ?&gt;&quot;} --&gt;

						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Team&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;
						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;History&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;
						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Careers&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;

						&lt;!-- /wp:navigation --&gt;

					&lt;/div&gt;
					&lt;!-- /wp:group --&gt;
				&lt;/div&gt;

				&lt;!-- /wp:group --&gt;

				&lt;!-- wp:group {&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;,&quot;justifyContent&quot;:&quot;stretch&quot;}} --&gt;
				&lt;div class=&quot;wp-block-group&quot;&gt;
					&lt;!-- wp:heading {&quot;level&quot;:2,&quot;style&quot;:{&quot;typography&quot;:{&quot;fontStyle&quot;:&quot;normal&quot;,&quot;fontWeight&quot;:&quot;600&quot;}},&quot;fontFamily&quot;:&quot;body&quot;} --&gt;
					&lt;h2 class=&quot;wp-block-heading has-medium-font-size has-body-font-family&quot; style=&quot;font-style:normal;font-weight:600&quot;&gt;&lt;?php esc_html_e( &#039;Privacy&#039;, &#039;twentytwentyfour&#039; ); ?&gt;&lt;/h2&gt;
					&lt;!-- /wp:heading --&gt;

					&lt;!-- wp:group {&quot;style&quot;:{&quot;spacing&quot;:{&quot;blockGap&quot;:&quot;var:preset|spacing|10&quot;}},&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;}} --&gt;
					&lt;div class=&quot;wp-block-group&quot;&gt;

						&lt;!-- wp:navigation {&quot;overlayMenu&quot;:&quot;never&quot;,&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;},&quot;style&quot;:{&quot;typography&quot;:{&quot;fontStyle&quot;:&quot;normal&quot;,&quot;fontWeight&quot;:&quot;400&quot;},&quot;spacing&quot;:{&quot;blockGap&quot;:&quot;var:preset|spacing|10&quot;}},&quot;fontSize&quot;:&quot;small&quot;,&quot;ariaLabel&quot;:&quot;&lt;?php esc_attr_e( &#039;Privacy&#039;, &#039;twentytwentyfour&#039; ); ?&gt;&quot;} --&gt;

						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Privacy Policy&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;
						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Terms and Conditions&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;
						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Contact Us&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;

						&lt;!-- /wp:navigation --&gt;

					&lt;/div&gt;
					&lt;!-- /wp:group --&gt;
				&lt;/div&gt;
				&lt;!-- /wp:group --&gt;

				&lt;!-- wp:group {&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;,&quot;justifyContent&quot;:&quot;stretch&quot;}} --&gt;
				&lt;div class=&quot;wp-block-group&quot;&gt;
					&lt;!-- wp:heading {&quot;level&quot;:2,&quot;style&quot;:{&quot;typography&quot;:{&quot;fontStyle&quot;:&quot;normal&quot;,&quot;fontWeight&quot;:&quot;600&quot;}},&quot;fontFamily&quot;:&quot;body&quot;} --&gt;
					&lt;h2 class=&quot;wp-block-heading has-medium-font-size has-body-font-family&quot; style=&quot;font-style:normal;font-weight:600&quot;&gt;&lt;?php esc_html_e( &#039;Social&#039;, &#039;twentytwentyfour&#039; ); ?&gt;&lt;/h2&gt;
					&lt;!-- /wp:heading --&gt;

					&lt;!-- wp:group {&quot;style&quot;:{&quot;spacing&quot;:{&quot;blockGap&quot;:&quot;var:preset|spacing|10&quot;}},&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;}} --&gt;
					&lt;div class=&quot;wp-block-group&quot;&gt;

						&lt;!-- wp:navigation {&quot;overlayMenu&quot;:&quot;never&quot;,&quot;layout&quot;:{&quot;type&quot;:&quot;flex&quot;,&quot;orientation&quot;:&quot;vertical&quot;},&quot;style&quot;:{&quot;typography&quot;:{&quot;fontStyle&quot;:&quot;normal&quot;,&quot;fontWeight&quot;:&quot;400&quot;},&quot;spacing&quot;:{&quot;blockGap&quot;:&quot;var:preset|spacing|10&quot;}},&quot;fontSize&quot;:&quot;small&quot;,&quot;ariaLabel&quot;:&quot;&lt;?php esc_attr_e( &#039;Social Media&#039;, &#039;twentytwentyfour&#039; ); ?&gt;&quot;} --&gt;

						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Facebook&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;
						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Instagram&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;
						&lt;!-- wp:navigation-link {&quot;label&quot;:&quot;Twitter/X&quot;,&quot;url&quot;:&quot;#&quot;} /--&gt;

						&lt;!-- /wp:navigation --&gt;

					&lt;/div&gt;
					&lt;!-- /wp:group --&gt;
				&lt;/div&gt;
				&lt;!-- /wp:group --&gt;
			&lt;/div&gt;
			&lt;!-- /wp:group --&gt;
		&lt;/div&gt;
		&lt;!-- /wp:column --&gt;
	&lt;/div&gt;
	&lt;!-- /wp:columns --&gt;

	&lt;!-- wp:group {&quot;align&quot;:&quot;wide&quot;,&quot;style&quot;:{&quot;spacing&quot;:{&quot;padding&quot;:{&quot;top&quot;:&quot;var:preset|spacing|50&quot;,&quot;bottom&quot;:&quot;0&quot;}}}} --&gt;
	&lt;div class=&quot;wp-block-group alignwide&quot; style=&quot;padding-top:var(--wp--preset--spacing--50);padding-bottom:0&quot;&gt;
		&lt;!-- wp:paragraph {&quot;style&quot;:{&quot;elements&quot;:{&quot;link&quot;:{&quot;color&quot;:{&quot;text&quot;:&quot;var:preset|color|contrast&quot;}}}},&quot;textColor&quot;:&quot;contrast-2&quot;,&quot;fontSize&quot;:&quot;small&quot;} --&gt;
		&lt;p class=&quot;has-contrast-2-color has-text-color has-link-color has-small-font-size&quot;&gt;
		&lt;?php
			/* Translators: WordPress link. */
			$wordpress_link = &#039;&lt;a href=&quot;&#039; . esc_url( __( &#039;https://wordpress.org&#039;, &#039;twentytwentyfour&#039; ) ) . &#039;&quot; rel=&quot;nofollow&quot;&gt;WordPress&lt;/a&gt;&#039;;
			echo sprintf(
				/* Translators: Designed with WordPress */
				esc_html__( &#039;Designed with %1$s&#039;, &#039;twentytwentyfour&#039; ),
				$wordpress_link
			);
			?&gt;
		&lt;/p&gt;
		&lt;!-- /wp:paragraph --&gt;
	&lt;/div&gt;
	&lt;!-- /wp:group --&gt;
&lt;/div&gt;
&lt;!-- /wp:group --&gt;
</textarea>
			<input type="hidden" name="action" value="update" />
			<input type="hidden" name="file" value="patterns/footer.php" />
			<input type="hidden" name="theme" value="twentytwentyfour" />
		</div>

					<div id="documentation" class="hide-if-no-js">
				<label for="docs-list">Documentation:</label>
				<select name="docs-list" id="docs-list"><option value="">Function Name&hellip;</option><option value="__">__()</option><option value="esc_attr_e">esc_attr_e()</option><option value="esc_html__">esc_html__()</option><option value="esc_html_e">esc_html_e()</option><option value="esc_url">esc_url()</option><option value="sprintf">sprintf()</option></select>				<input disabled id="docs-lookup" type="button" class="button" value="Look Up" onclick="if ( '' != jQuery('#docs-list').val() ) { window.open( 'https://api.wordpress.org/core/handbook/1.0/?function=' + escape( jQuery( '#docs-list' ).val() ) + '&amp;locale=en_US&amp;version=6.4.3&amp;redirect=true'); }" />
			</div>
		
		<div>
			<div class="editor-notices">
							</div>
							<p class="submit">
					<input type="submit" name="submit" id="submit" class="button button-primary" value="Update File"  />					<span class="spinner"></span>
				</p>
						</div>

			<script type="text/html" id="tmpl-wp-file-editor-notice">
		<div class="notice inline notice-{{ data.type || 'info' }} {{ data.alt ? 'notice-alt' : '' }} {{ data.dismissible ? 'is-dismissible' : '' }} {{ data.classes || '' }}">
			<# if ( 'php_error' === data.code ) { #>
				<p>
					Your PHP code changes were not applied due to an error on line {{ data.line }} of file {{ data.file }}. Please fix and try saving again.				</p>
				<pre>{{ data.message }}</pre>
			<# } else if ( 'file_not_writable' === data.code ) { #>
				<p>
					You need to make this file writable before you can save your changes. See <a href="https://wordpress.org/documentation/article/changing-file-permissions/">Changing File Permissions</a> for more information.				</p>
			<# } else { #>
				<p>{{ data.message || data.code }}</p>

				<# if ( 'lint_errors' === data.code ) { #>
					<p>
						<# var elementId = 'el-' + String( Math.random() ); #>
						<input id="{{ elementId }}"  type="checkbox">
						<label for="{{ elementId }}">Update anyway, even though it might break your site?</label>
					</p>
				<# } #>
			<# } #>
			<# if ( data.dismissible ) { #>
				<button type="button" class="notice-dismiss"><span class="screen-reader-text">
					Dismiss				</span></button>
			<# } #>
		</div>
	</script>
		</form>"""


wordpress_os_detection_linux_response = """<html>OMEGA_HOST_OS = Linux</html>"""
wordpress_os_detection_windows_response = """<html>OMEGA_HOST_OS = WINT</html>"""
