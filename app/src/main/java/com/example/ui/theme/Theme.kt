package com.example.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val HighDensityColorScheme = lightColorScheme(
    primary = HighDensityPrimary,
    onPrimary = HighDensitySurface,
    primaryContainer = HighDensityPrimaryContainer,
    onPrimaryContainer = HighDensityOnPrimaryContainer,
    secondary = HighDensityPrimaryDark,
    onSecondary = HighDensitySurface,
    secondaryContainer = HighDensitySurfaceVariant,
    onSecondaryContainer = HighDensityPrimaryDark,
    tertiary = HighDensitySuccess,
    background = HighDensityBg,
    onBackground = HighDensityTextPrimary,
    surface = HighDensitySurface,
    onSurface = HighDensityTextPrimary,
    surfaceVariant = HighDensitySurfaceVariant,
    onSurfaceVariant = HighDensityTextSecondary,
    outline = HighDensityBorder,
    error = HighDensityDanger
)

private val HighDensityDarkScheme = darkColorScheme(
    primary = HighDensityPrimary,
    onPrimary = HighDensitySurface,
    primaryContainer = HighDensitySurfaceVariant,
    onPrimaryContainer = HighDensityPrimaryContainer,
    secondary = HighDensityPrimaryContainer,
    onSecondary = HighDensityPrimaryDark,
    tertiary = HighDensitySuccess,
    background = HighDensityDarkCard,
    onBackground = HighDensityDarkCardText,
    surface = HighDensityDarkCard,
    onSurface = HighDensityDarkCardText,
    surfaceVariant = HighDensitySurfaceVariant,
    onSurfaceVariant = HighDensityTextSecondary,
    outline = HighDensityBorder,
    error = HighDensityDanger
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = false, // High Density defaults to clean warm light canvas
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit,
) {
    val colorScheme = if (darkTheme) HighDensityDarkScheme else HighDensityColorScheme
    MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}


