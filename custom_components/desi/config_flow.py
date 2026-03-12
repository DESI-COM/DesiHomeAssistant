"""Config flow for Desi OAuth2 integration."""

import logging
import voluptuous as vol
import jwt  # type: ignore  # noqa: PGH003

from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers import config_entry_oauth2_flow

from .const import AUTH_URI, DOMAIN, TOKEN_URI

_LOGGER = logging.getLogger(__name__)

class DesiConfigFlow(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN):
    """Desi Smart OAuth2 Flow."""

    VERSION = 1
    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Logger."""
        return _LOGGER

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle a flow initialized by the user from the integrations page."""
        
        # 1. ADIM: Kullanıcı entegrasyonu seçtiğinde karşısına boş bir onay formu çıkar.
        # Bu form, mobil uygulamanın otomatik yönlendirme yapmasını engeller.
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({}),
            )

        # 2. ADIM: Kullanıcı 'GÖNDER' butonuna bastıysa, OAuth implementasyonunu hazırla.
        implementations = await config_entry_oauth2_flow.async_get_implementations(
            self.hass, DOMAIN
        )

        if not implementations:
            config_entry_oauth2_flow.async_register_implementation(
                self.hass,
                DOMAIN,
                config_entry_oauth2_flow.LocalOAuth2Implementation(
                    self.hass, DOMAIN, "", "", AUTH_URI, TOKEN_URI
                ),
            )

            implementations = await config_entry_oauth2_flow.async_get_implementations(
                self.hass, DOMAIN
            )

        self.flow_impl = list(implementations.values())[0]

        # 3. ADIM: Artık tarayıcıyı açması için komut veriyoruz.
        # Mobil uygulama bu noktada 'OPEN WEBSITE' butonunu gösterecektir.
        return await self.async_step_auth()

    async def async_oauth_create_entry(self, data: dict) -> ConfigFlowResult:
        """Create an entry after successful OAuth authentication and token retrieval."""
        try:
            # Token içinden user_id (sub) bilgisini çıkar
            token_data = data["token"]["access_token"]
            decoded = jwt.decode(token_data, options={"verify_signature": False})
            user_id = decoded["sub"]

            await self.async_set_unique_id(user_id)
            self._abort_if_unique_id_configured()

        except (jwt.InvalidTokenError, KeyError):
            _LOGGER.exception("Failed to parse token or extract user ID during setup")
            return self.async_abort(reason="oauth_error")

        else:
            return self.async_create_entry(title=f"Desi Smart ({user_id})", data=data)