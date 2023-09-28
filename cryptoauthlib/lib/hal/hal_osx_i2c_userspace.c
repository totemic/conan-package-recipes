/**
 * \file
 * \brief ATCA Hardware abstraction layer for OSX that simulates I2C. Adapted from hal_linux_i2c_userspace
 */

#include <cryptoauthlib.h>

#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "atca_hal.h"

/** \defgroup hal_ Hardware abstraction layer (hal_)
 *
 * \brief
 * These methods define the hardware abstraction layer for communicating with a CryptoAuth device
 *
   @{ */

typedef struct atca_i2c_host_s
{
    char i2c_file[16];
    int  ref_ct;
} atca_i2c_host_t;

/** \brief HAL implementation of I2C init
 *
 * this implementation assumes I2C peripheral has been enabled by user. It only initialize an
 * I2C interface using given config.
 *
 *  \param[in] hal pointer to HAL specific data that is maintained by this HAL
 *  \param[in] cfg pointer to HAL specific configuration data that is used to initialize this HAL
 * \return ATCA_SUCCESS on success, otherwise an error code.
 */

ATCA_STATUS hal_i2c_init(ATCAIface iface, ATCAIfaceCfg* cfg)
{
    ATCA_STATUS ret = ATCA_BAD_PARAM;

    if ((NULL == iface) || (NULL == cfg))
    {
        return ret;
    }

    if (NULL != iface->hal_data)
    {
        atca_i2c_host_t * hal_data = (atca_i2c_host_t*)iface->hal_data;

        // Assume the bus had already been initialized
        hal_data->ref_ct++;

        ret = ATCA_SUCCESS;
    }
    else
    {
        /* coverity[misra_c_2012_directive_4_12_violation] Intentional as it is required for the linux environment */
        /* coverity[misra_c_2012_rule_21_3_violation] Intentional as it is required for the linux environment */
        if (NULL != (iface->hal_data = malloc(sizeof(atca_i2c_host_t))))
        {
            atca_i2c_host_t * hal_data = (atca_i2c_host_t*)iface->hal_data;
            int bus = (int)ATCA_IFACECFG_VALUE(cfg, atcai2c.bus); // 0-based logical bus number

            hal_data->ref_ct = 1;                                 // buses are shared, this is the first instance

            /* coverity[misra_c_2012_rule_21_6_violation] snprintf is approved for formatted string writes to buffers */
            (void)snprintf(hal_data->i2c_file, sizeof(hal_data->i2c_file) - 1U, "/dev/i2c-%d", bus);

            ret = ATCA_SUCCESS;
        }
        else
        {
            ret = ATCA_ALLOC_FAILURE;
        }
    }

    return ret;

}

/** \brief HAL implementation of I2C post init
 * \param[in] iface  instance
 * \return ATCA_SUCCESS on success, otherwise an error code.
 */
ATCA_STATUS hal_i2c_post_init(ATCAIface iface)
{
    ((void)iface);
    return ATCA_SUCCESS;
}

/** \brief HAL implementation of I2C send
 * \param[in] iface         instance
 * \param[in] word_address  device transaction type
 * \param[in] txdata        pointer to space to bytes to send
 * \param[in] txlength      number of bytes to send
 * \return ATCA_SUCCESS on success, otherwise an error code.
 */
ATCA_STATUS hal_i2c_send(ATCAIface iface, uint8_t word_address, uint8_t *txdata, int txlength)
{
    return ATCA_SUCCESS;
}

/** \brief HAL implementation of I2C receive function
 * \param[in]    iface          Device to interact with.
 * \param[in]    address        device address
 * \param[out]   rxdata         Data received will be returned here.
 * \param[in,out] rxlength      As input, the size of the rxdata buffer.
 *                              As output, the number of bytes received.
 * \return ATCA_SUCCESS on success, otherwise an error code.
 */
ATCA_STATUS hal_i2c_receive(ATCAIface iface, uint8_t word_address, uint8_t *rxdata, uint16_t *rxlength)
{
    return ATCA_SUCCESS;
}

/** \brief Perform control operations for the kit protocol
 * \param[in]     iface          Interface to interact with.
 * \param[in]     option         Control parameter identifier
 * \param[in]     param          Optional pointer to parameter value
 * \param[in]     paramlen       Length of the parameter
 * \return ATCA_SUCCESS on success, otherwise an error code.
 */
ATCA_STATUS hal_i2c_control(ATCAIface iface, uint8_t option, void* param, size_t paramlen)
{
    return ATCA_UNIMPLEMENTED;
}

/** \brief manages reference count on given bus and releases resource if no more refences exist
 * \param[in] hal_data - opaque pointer to hal data structure - known only to the HAL implementation
 * \return ATCA_SUCCESS on success, otherwise an error code.
 */
ATCA_STATUS hal_i2c_release(void *hal_data)
{
    atca_i2c_host_t *hal = (atca_i2c_host_t*)hal_data;

    if (NULL != hal)
    {
        // if the use count for this bus has gone to 0 references, disable it.  protect against an unbracketed release
        if (0 < hal->ref_ct)
        {
            hal->ref_ct--;
        }

        if (0 == hal->ref_ct)
        {
            /* coverity[misra_c_2012_rule_21_3_violation] Intentional as it is required for the linux environment */
            free(hal);
        }
    }

    return ATCA_SUCCESS;
}

/** @} */
